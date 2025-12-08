"""
BeatSync PRO - Premium Lip Sync (FAL AI PixVerse)
"""
import os, time, logging, subprocess, requests
import fal_client
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LipSyncResult:
    success: bool
    output_path: Optional[str] = None
    error: Optional[str] = None
    credits_used: int = 0
    job_id: Optional[str] = None

class LipSyncAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('FAL_KEY')
        if self.api_key:
            os.environ['FAL_KEY'] = self.api_key
        self.temp_dir = Path(os.environ.get('TEMP', '/tmp')) / '.beatsync' / 'lipsync_temp'
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        print("LipSyncAPI initialized (FAL AI PixVerse)")

    def _get_video_duration(self, video_path: str) -> float:
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', video_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return float(result.stdout.strip())
        except:
            return 10.0

    def _trim_audio(self, audio_path: str, duration: float) -> str:
        output = self.temp_dir / f'audio_trim_{hash(audio_path) % 10000}.mp3'
        cmd = ['ffmpeg', '-y', '-i', audio_path, '-t', str(duration + 0.5), '-c:a', 'libmp3lame', '-b:a', '192k', str(output)]
        subprocess.run(cmd, capture_output=True, timeout=60)
        return str(output)

    def process_video(self, video_path: str, audio_path: str, quality: str = "standard", progress_callback=None) -> LipSyncResult:
        print(f"Starting FAL AI PixVerse lip sync: {Path(video_path).name}")
        start = time.time()
        
        if not self.api_key:
            return LipSyncResult(success=False, error="FAL_KEY not configured")
        
        try:
            if progress_callback:
                progress_callback(5, "Preparing files...")
            
            duration = self._get_video_duration(video_path)
            trimmed_audio = self._trim_audio(audio_path, duration)
            
            if progress_callback:
                progress_callback(15, "Uploading to cloud...")
            
            print(f"[UPLOAD] Uploading video: {Path(video_path).name}")
            video_url = fal_client.upload_file(video_path)
            print(f"[UPLOAD] Uploading audio...")
            audio_url = fal_client.upload_file(trimmed_audio)
            
            if progress_callback:
                progress_callback(30, "Processing lip sync...")
            
            print(f"[API] Submitting to FAL AI PixVerse...")
            result = fal_client.subscribe(
                'fal-ai/pixverse/lipsync',
                arguments={
                    'video_url': video_url,
                    'audio_url': audio_url
                },
                with_logs=False
            )
            
            output_url = result.get('video', {}).get('url')
            if not output_url:
                return LipSyncResult(success=False, error="No output URL in response")
            
            if progress_callback:
                progress_callback(85, "Downloading result...")
            
            print(f"[API] SUCCESS - Downloading result...")
            response = requests.get(output_url, timeout=120)
            
            output_path = self.temp_dir / f'lipsync_{int(time.time())}.mp4'
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            credits = int(duration * 10)
            print(f"[API] SUCCESS: {output_path}")
            
            if progress_callback:
                progress_callback(100, "Complete!")
            
            return LipSyncResult(
                success=True,
                output_path=str(output_path),
                credits_used=credits
            )
            
        except Exception as e:
            print(f"[API] ERROR: {e}")
            return LipSyncResult(success=False, error=str(e))
    
    # Alias for compatibility
    sync_video = process_video
    
    @staticmethod
    def estimate_cost(duration_seconds: float, quality: str = "standard") -> dict:
        credits = int(duration_seconds * 10)
        return {'credits': credits, 'dollars': duration_seconds * 0.04}
    
    def get_api_status(self):
        if not self.api_key:
            return {'status': 'error', 'message': 'FAL_KEY not configured'}
        return {'status': 'ok', 'message': 'FAL AI PixVerse ready'}

if __name__ == "__main__":
    api = LipSyncAPI()
    print(f"Status: {api.get_api_status()}")
