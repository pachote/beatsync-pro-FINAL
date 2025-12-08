"""
BeatSync PRO - Lip Sync API Integration
Real implementation of Sync.so API for photorealistic lip sync
"""

import os
import time
import json
import logging
import hashlib
import requests
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LipSyncResult:
    """Result from lip sync API"""
    success: bool
    output_path: Optional[str] = None
    error: Optional[str] = None
    credits_used: int = 0
    processing_time: float = 0.0


class LipSyncAPI:
    """
    Lip Sync API Integration for BeatSync PRO
    
    Providers:
    - sync_labs: Sync.so API (Primary - Best quality)
    - beta_api: Reserved for future beta API integration
    """
    
    # API Endpoints
    SYNC_LABS_BASE = "https://api.sync.so"
    
    # Cost per second (approximate)
    COST_PER_SECOND = {
        'sync_labs_standard': 0.05,
        'sync_labs_pro': 0.10,
        'beta_api': 0.03,
    }
    
    def __init__(self, api_key: Optional[str] = None, provider: str = 'sync_labs'):
        self.api_key = api_key or os.getenv('SYNC_LABS_API_KEY')
        self.provider = provider
        
        self.cache_dir = Path('cache/lipsync')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.temp_dir = Path.home() / '.beatsync' / 'lipsync_temp'
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.api_key:
            logger.warning("No Sync Labs API key. Set SYNC_LABS_API_KEY env var.")
    
    def _get_cache_key(self, video_path: str, audio_path: str, quality: str) -> str:
        video_stat = os.stat(video_path)
        audio_stat = os.stat(audio_path)
        key_data = f"{video_path}_{video_stat.st_mtime}_{audio_path}_{audio_stat.st_mtime}_{quality}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _check_cache(self, cache_key: str) -> Optional[str]:
        cache_file = self.cache_dir / f"{cache_key}.mp4"
        if cache_file.exists():
            logger.info(f"Cache hit: {cache_key}")
            return str(cache_file)
        return None
    

    def _compress_for_upload(self, video_path: str, max_size_mb: float = 0.15):
        """Compress video for API upload - max 720p, target size"""
        import subprocess
        from pathlib import Path
        
        input_path = Path(video_path)
        output_path = self.temp_dir / f'upload_{input_path.stem}.mp4'
        
        # Check if already small enough
        file_size_mb = input_path.stat().st_size / (1024 * 1024)
        if file_size_mb <= max_size_mb:
            logger.info(f'Video already small enough: {file_size_mb:.1f}MB')
            return None
        
        logger.info(f'Compressing {file_size_mb:.1f}MB video for upload...')
        
        # FFmpeg compress to 720p with aggressive settings
        cmd = [
            'ffmpeg', '-y', '-i', str(video_path),
            '-vf', 'scale=-2:360',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '38',
            '-c:a', 'aac', '-b:a', '24k',
            '-movflags', '+faststart',
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)
            new_size = output_path.stat().st_size / (1024 * 1024)
            logger.info(f'Compressed to {new_size:.1f}MB')
            return str(output_path)
        except Exception as e:
            logger.warning(f'Compression failed: {e}')
            return None


    def _trim_audio_for_clip(self, audio_path: str, duration: float) -> str:
            """Trim audio to match video clip duration"""
            import subprocess
            import os
            from pathlib import Path
            
            output_path = self.temp_dir / f'audio_trim_{hash(audio_path) % 10000}.mp3'
            
            # Log input size
            try:
                input_size = os.path.getsize(audio_path) / 1024 / 1024
                print(f"[AUDIO TRIM] Input: {input_size:.2f}MB, Duration target: {duration:.1f}s")
            except:
                print(f"[AUDIO TRIM] Starting trim for duration: {duration:.1f}s")
            
            cmd = [
                'ffmpeg', '-y', '-i', str(audio_path),
                '-t', str(duration),
                '-ac', '1', '-ar', '16000', '-c:a', 'libmp3lame', '-b:a', '64k',
                str(output_path)
            ]
            
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, timeout=30)
                output_size = os.path.getsize(output_path) / 1024
                print(f"[AUDIO TRIM] SUCCESS: {output_size:.1f}KB -> {output_path}")
                return str(output_path)
            except Exception as e:
                print(f"[AUDIO TRIM] FAILED: {e}")
                logger.warning(f'Audio trim failed: {e}')
                return audio_path
    def sync_video(
        self, 
        video_path: str, 
        audio_path: str,
        quality: str = 'standard',
        progress_callback: Optional[callable] = None
    ) -> LipSyncResult:
        """Sync video lips to audio"""
        start_time = time.time()
        
        # Check cache
        cache_key = self._get_cache_key(video_path, audio_path, quality)
        cached = self._check_cache(cache_key)
        if cached:
            return LipSyncResult(success=True, output_path=cached, credits_used=0)
        
        if self.provider == 'sync_labs':
            result = self._sync_labs_api(video_path, audio_path, quality, progress_callback)
        elif self.provider == 'beta_api':
            result = self._beta_api(video_path, audio_path, quality, progress_callback)
        else:
            return LipSyncResult(success=False, error=f"Unknown provider: {self.provider}")
        
        result.processing_time = time.time() - start_time
        return result
    
    def _sync_labs_api(
        self, 
        video_path: str, 
        audio_path: str,
        quality: str = 'standard',
        progress_callback: Optional[callable] = None
    ) -> LipSyncResult:
        """Sync Labs (Sync.so) API Implementation"""
        if not self.api_key:
            return LipSyncResult(
                success=False, 
                error="No Sync Labs API key. Set SYNC_LABS_API_KEY environment variable."
            )
        
        logger.info(f"Starting Sync Labs lip sync: {Path(video_path).name}")
        if progress_callback:
            progress_callback(5, "Preparing files...")
        
        try:
            import base64
            
            # Compress video for API upload (max 720p, 2MB target)
            compressed_path = self._compress_for_upload(video_path)
            upload_path = compressed_path if compressed_path else video_path
            
            with open(upload_path, 'rb') as f:
                video_b64 = base64.b64encode(f.read()).decode('utf-8')
            
            # Get video duration and trim audio to match
            import subprocess
            probe = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', upload_path],
                capture_output=True, text=True
            )
            video_duration = float(probe.stdout.strip()) if probe.stdout.strip() else 10.0
            
            trimmed_audio = self._trim_audio_for_clip(audio_path, video_duration)
            with open(trimmed_audio, 'rb') as f:
                audio_b64 = base64.b64encode(f.read()).decode('utf-8')
            
            if progress_callback:
                progress_callback(15, "Submitting to Sync Labs API...")
            
            model = "lipsync-2" if quality == 'standard' else "lipsync-2-pro"
            
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': model,
                'input': [
                    {'type': 'video', 'data': f'data:video/mp4;base64,{video_b64}'},
                    {'type': 'audio', 'data': f'data:audio/mpeg;base64,{audio_b64}'}
                ],
                'options': {'sync_mode': 'cut_off'}
            }
            # Log payload size for debugging
            import json as _json
            _payload_str = _json.dumps(payload)
            print(f"[API] Payload size: {len(_payload_str)/1024/1024:.2f}MB")
            print(f"[API] Video b64: {len(video_b64)//1024}KB, Audio b64: {len(audio_b64)//1024}KB")
            
            response = requests.post(
                f"{self.SYNC_LABS_BASE}/v2/generate",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code not in (200, 201):
                print(f"[API] Error {response.status_code}: {response.text[:500]}"); return LipSyncResult(success=False, error=f"API error {response.status_code}: {response.text[:200]}")
            
            result = response.json()
            job_id = result.get('id')
            
            if not job_id:
                return LipSyncResult(success=False, error="No job ID returned")
            
            logger.info(f"Job submitted: {job_id}")
            return self._poll_job(job_id, headers, progress_callback)
            
        except Exception as e:
            logger.exception("Sync Labs API error")
            return LipSyncResult(success=False, error=str(e))
    
    def _poll_job(self, job_id: str, headers: dict, progress_callback=None, max_wait=600):
        """Poll for job completion"""
        start = time.time()
        progress = 25
        
        while time.time() - start < max_wait:
            try:
                resp = requests.get(f"{self.SYNC_LABS_BASE}/v2/generate/{job_id}", headers=headers, timeout=30)
                
                if resp.status_code != 200:
                    time.sleep(5)
                    continue
                
                data = resp.json()
                status = data.get('status', '').lower()
                
                if status == 'processing':
                    progress = min(progress + 5, 85)
                    if progress_callback:
                        progress_callback(progress, "Processing...")
                
                elif status == 'completed':
                    if progress_callback:
                        progress_callback(90, "Downloading...")
                    
                    output_url = data.get('output', {}).get('url') or data.get('outputUrl')
                    if not output_url:
                        return LipSyncResult(success=False, error="No output URL")
                    
                    output_path = self.temp_dir / f"lipsync_{job_id}.mp4"
                    video_data = requests.get(output_url, timeout=120)
                    output_path.write_bytes(video_data.content)
                    
                    if progress_callback:
                        progress_callback(100, "Complete!")
                    
                    return LipSyncResult(success=True, output_path=str(output_path), credits_used=data.get('credits', 0))
                
                elif status == 'failed':
                    return LipSyncResult(success=False, error=data.get('error', 'Job failed'))
                
            except Exception as e:
                logger.warning(f"Poll error: {e}")
            
            time.sleep(5)
        
        return LipSyncResult(success=False, error="Job timed out")
    
    def _beta_api(self, video_path, audio_path, quality, progress_callback):
        """Beta API placeholder"""
        return LipSyncResult(success=False, error="Beta API not yet available")
    
    @staticmethod
    def estimate_cost(duration_sec: float, provider: str = 'sync_labs', quality: str = 'standard') -> Dict:
        key = f"{provider}_{quality}"
        cost_per_sec = LipSyncAPI.COST_PER_SECOND.get(key, 0.05)
        dollar_cost = duration_sec * cost_per_sec
        return {'credits': int(dollar_cost * 100), 'dollars': dollar_cost}
    
    def get_api_status(self) -> Dict:
        if not self.api_key:
            return {'status': 'error', 'message': 'No API key'}
        return {'status': 'ok', 'message': 'API key configured'}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    api = LipSyncAPI()
    print(f"API Status: {api.get_api_status()}")
    print(f"30 sec estimate: {LipSyncAPI.estimate_cost(30)}")








