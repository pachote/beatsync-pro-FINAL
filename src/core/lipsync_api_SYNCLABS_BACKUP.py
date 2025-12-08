"""
Sync Labs (Sync.so) Lip Sync API - MULTIPART UPLOAD VERSION
Uses multipart/form-data for file upload (NOT base64)
"""
import os
import time
import logging
import requests
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LipSyncResult:
    success: bool
    output_path: Optional[str] = None
    error: Optional[str] = None
    job_id: Optional[str] = None
    credits_used: int = 0


class LipSyncAPI:
    """Sync Labs API using multipart/form-data upload (NOT base64)"""
    
    API_BASE = "https://api.sync.so/v2"
    
    def __init__(self):
        self.api_key = os.environ.get('SYNC_LABS_API_KEY', '')
        self.temp_dir = Path(tempfile.gettempdir()) / '.beatsync' / 'lipsync_temp'
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.api_key:
            logger.warning("No Sync Labs API key. Set SYNC_LABS_API_KEY env var.")
        
        print("LipSyncAPI initialized (Sync Labs - Multipart Upload)")
    
    def _compress_video(self, video_path: str, max_size_mb: float = 10.0) -> str:
        """Compress video for upload - can be larger since no base64"""
        input_path = Path(video_path)
        file_size_mb = input_path.stat().st_size / (1024 * 1024)
        
        print(f"Compressing {file_size_mb:.1f}MB video for upload...")
        
        if file_size_mb <= max_size_mb:
            print(f"Video already under {max_size_mb}MB, using as-is")
            return video_path
        
        output_path = self.temp_dir / f'compressed_{input_path.stem}.mp4'
        
        cmd = [
            'ffmpeg', '-y', '-i', str(video_path),
            '-vf', 'scale=-2:min(ih\,720)',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
            '-c:a', 'aac', '-b:a', '128k',
            '-movflags', '+faststart',
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)
            new_size = output_path.stat().st_size / (1024 * 1024)
            print(f"Compressed to {new_size:.1f}MB")
            return str(output_path)
        except Exception as e:
            logger.warning(f"Compression failed: {e}, using original")
            return video_path
    
    def _trim_audio(self, audio_path: str, duration: float) -> str:
        """Trim audio to match video duration"""
        output_path = self.temp_dir / f'audio_trim_{hash(audio_path) % 10000}.mp3'
        
        input_size = Path(audio_path).stat().st_size / (1024 * 1024)
        print(f"[AUDIO TRIM] Input: {input_size:.2f}MB, Duration target: {duration:.1f}s")
        
        cmd = [
            'ffmpeg', '-y', '-i', str(audio_path),
            '-t', str(duration),
            '-ac', '1',
            '-ar', '16000',
            '-c:a', 'libmp3lame', '-b:a', '128k',
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=60)
            new_size = output_path.stat().st_size / 1024
            print(f"[AUDIO TRIM] SUCCESS: {new_size:.1f}KB -> {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Audio trim failed: {e}")
            return audio_path
    
    def _get_video_duration(self, video_path: str) -> float:
        """Get video duration using ffprobe"""
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return float(result.stdout.strip())
        except:
            return 10.0
    
    def sync_video(self, video_path: str, audio_path: str, output_path: str = None, model: str = 'lipsync-2', progress_callback = None):
        return self.process_video(video_path, audio_path, output_path, model, progress_callback)

    def process_video(self, video_path: str, audio_path: str, quality: str = "standard",
        output_path: Optional[str] = None,
        model: str = "lipsync-2",
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> LipSyncResult:
        """Process video with Sync Labs API using multipart upload"""
        
        if not self.api_key:
            return LipSyncResult(
                success=False,
                error="No Sync Labs API key. Set SYNC_LABS_API_KEY environment variable."
            )
        
        logger.info(f"Starting Sync Labs lip sync: {Path(video_path).name}")
        print(f"Starting Sync Labs lip sync: {Path(video_path).name}")
        
        try:
            if progress_callback:
                progress_callback(5, "Compressing video...")
            
            compressed_video = self._compress_video(video_path, max_size_mb=50.0)
            
            if progress_callback:
                progress_callback(10, "Preparing audio...")
            
            video_duration = self._get_video_duration(compressed_video)
            trimmed_audio = self._trim_audio(audio_path, video_duration)
            
            video_size = Path(compressed_video).stat().st_size / 1024
            audio_size = Path(trimmed_audio).stat().st_size / 1024
            print(f"[UPLOAD] Video: {video_size:.0f}KB, Audio: {audio_size:.0f}KB")
            
            if progress_callback:
                progress_callback(15, "Uploading to Sync Labs API...")
            
            # MULTIPART FORM DATA - NOT BASE64!
            files = {
                'video': ('video.mp4', open(compressed_video, 'rb'), 'video/mp4'),
                'audio': ('audio.mp3', open(trimmed_audio, 'rb'), 'audio/mpeg'),
            }
            
            data = {
                'model': model,
                'options': '{"sync_mode":"cut_off"}'
            }
            
            headers = {
                'x-api-key': self.api_key
            }
            
            print(f"[API] Submitting multipart request to {self.API_BASE}/generate")
            
            response = requests.post(
                f"{self.API_BASE}/generate",
                headers=headers,
                files=files,
                data=data,
                timeout=120
            )
            
            for f in files.values():
                f[1].close()
            
            print(f"[API] Response status: {response.status_code}")
            
            if response.status_code == 413:
                print(f"[API] Error 413: {response.text}")
                return LipSyncResult(success=False, error=f"API error 413: {response.text}")
            
            if response.status_code != 200 and response.status_code != 201:
                print(f"[API] Error {response.status_code}: {response.text}")
                return LipSyncResult(success=False, error=f"API error {response.status_code}: {response.text}")
            
            result = response.json()
            job_id = result.get('id')
            print(f"[API] Job submitted: {job_id}")
            
            if progress_callback:
                progress_callback(20, f"Processing... Job: {job_id}")
            
            max_wait = 300
            poll_interval = 5
            elapsed = 0
            
            while elapsed < max_wait:
                status_response = requests.get(
                    f"{self.API_BASE}/generate/{job_id}",
                    headers=headers,
                    timeout=30
                )
                
                if status_response.status_code != 200:
                    time.sleep(poll_interval)
                    elapsed += poll_interval
                    continue
                
                status_data = status_response.json()
                status = status_data.get('status', '')
                
                print(f"[API] Status: {status}")
                
                if status == 'COMPLETED':
                    output_url = status_data.get('outputUrl')
                    if output_url:
                        if progress_callback:
                            progress_callback(90, "Downloading result...")
                        
                        if not output_path:
                            output_path = str(self.temp_dir / f'lipsync_{job_id}.mp4')
                        
                        video_response = requests.get(output_url, timeout=120)
                        with open(output_path, 'wb') as f:
                            f.write(video_response.content)
                        
                        print(f"[API] SUCCESS: {output_path}")
                        
                        if progress_callback:
                            progress_callback(100, "Complete!")
                        
                        return LipSyncResult(
                            success=True,
                            output_path=output_path,
                            job_id=job_id,
                            credits_used=int(video_duration)
                        )
                
                elif status == 'FAILED':
                    error_msg = status_data.get('error', 'Unknown error')
                    print(f"[API] FAILED: {error_msg}")
                    return LipSyncResult(success=False, error=f"Processing failed: {error_msg}", job_id=job_id)
                
                progress_pct = min(85, 20 + int(elapsed / max_wait * 65))
                if progress_callback:
                    progress_callback(progress_pct, f"Processing... ({elapsed}s)")
                
                time.sleep(poll_interval)
                elapsed += poll_interval
            
            return LipSyncResult(success=False, error="Timeout waiting for processing", job_id=job_id)
            
        except requests.exceptions.RequestException as e:
            logger.exception("Sync Labs API request error")
            print(f"[API] Request error: {e}")
            return LipSyncResult(success=False, error=str(e))
        except Exception as e:
            logger.exception("Sync Labs API error")
            print(f"[API] Error: {e}")
            return LipSyncResult(success=False, error=str(e))
    
    @staticmethod
    def estimate_cost(duration_sec: float, model: str = "lipsync-2") -> Dict:
        cost_per_sec = 0.02 if model == "lipsync-2" else 0.03
        dollar_cost = duration_sec * cost_per_sec
        return {'credits': int(dollar_cost * 100), 'dollars': dollar_cost}
    
    def get_api_status(self) -> Dict:
        if not self.api_key:
            return {'status': 'error', 'message': 'No API key'}
        return {'status': 'ok', 'message': 'API key configured'}


    # Alias for compatibility
    sync_video = process_video

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    api = LipSyncAPI()
    print(f"API Status: {api.get_api_status()}")
    print(f"30 sec estimate: {LipSyncAPI.estimate_cost(30)}")



