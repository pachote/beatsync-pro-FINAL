"""
BeatSync PRO - Premium Lip Sync Integration
"""
import os, time, logging, hashlib, requests, subprocess, fal_client
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LipSyncResult:
    success: bool
    output_path: Optional[str] = None
    error: Optional[str] = None
    credits_used: int = 0
    processing_time: float = 0.0

class LipSyncAPI:
    COST_PER_SECOND = {'standard': 0.04}
    USER_CREDITS_PER_SECOND = 10

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('FAL_KEY')
        if self.api_key: os.environ['FAL_KEY'] = self.api_key
        self.cache_dir = Path('cache/lipsync')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path.home() / '.beatsync' / 'lipsync_temp'
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, video_path, audio_path, quality):
        v, a = os.stat(video_path), os.stat(audio_path)
        return hashlib.md5(f"{video_path}_{v.st_mtime}_{audio_path}_{a.st_mtime}_{quality}".encode()).hexdigest()

    def _check_cache(self, cache_key):
        f = self.cache_dir / f"{cache_key}.mp4"
        return str(f) if f.exists() else None

    def _save_to_cache(self, cache_key, data):
        f = self.cache_dir / f"{cache_key}.mp4"
        f.write_bytes(data)
        return str(f)

    def _trim_audio(self, audio_path, duration):
        out = self.temp_dir / f'trim_{hash(audio_path)%10000}.mp3'
        try:
            subprocess.run(['ffmpeg','-y','-i',str(audio_path),'-t',str(duration),'-c:a','libmp3lame','-b:a','128k',str(out)], check=True, capture_output=True, timeout=30)
            return str(out)
        except: return audio_path

    def _get_duration(self, video_path):
        try:
            r = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',video_path], capture_output=True, text=True, timeout=30)
            return float(r.stdout.strip()) if r.stdout.strip() else 10.0
        except: return 10.0

    def sync_video(self, video_path, audio_path, quality='standard', progress_callback=None):
        start = time.time()
        ck = self._get_cache_key(video_path, audio_path, quality)
        if c := self._check_cache(ck): return LipSyncResult(success=True, output_path=c, credits_used=0)
        if not self.api_key: return LipSyncResult(success=False, error="Not configured")
        try:
            if progress_callback: progress_callback(5, "Preparing...")
            dur = self._get_duration(video_path)
            audio = self._trim_audio(audio_path, dur)
            if progress_callback: progress_callback(15, "Uploading...")
            v_url = fal_client.upload_file(video_path)
            a_url = fal_client.upload_file(audio)
            if progress_callback: progress_callback(30, "Processing...")
            result = fal_client.subscribe('fal-ai/pixverse/lipsync', arguments={'video_url': v_url, 'audio_url': a_url}, with_logs=False)
            if progress_callback: progress_callback(85, "Downloading...")
            url = result.get('video', {}).get('url')
            if not url: return LipSyncResult(success=False, error="No output")
            r = requests.get(url, timeout=120)
            out = self._save_to_cache(ck, r.content)
            if progress_callback: progress_callback(100, "Complete!")
            return LipSyncResult(success=True, output_path=out, credits_used=int(dur*10), processing_time=time.time()-start)
        except Exception as e: return LipSyncResult(success=False, error=str(e))

    @staticmethod
    def estimate_cost(duration_sec, quality='standard'):
        return {'credits': int(duration_sec * 10), 'dollars': duration_sec * 0.04}

    def get_api_status(self):
        return {'status': 'ok', 'message': 'Ready'} if self.api_key else {'status': 'error', 'message': 'Not configured'}

