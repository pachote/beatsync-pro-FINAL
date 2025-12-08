"""
BeatSync PRO - Lip Sync Integration Layer
Connects vocal separation and FAL AI PixVerse lip sync API
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class LipSyncIntegration:
    """Integrates lip sync into video rendering pipeline"""

    def __init__(self, quality: str = 'local', gender: str = 'female'):
        self.quality = quality
        self.gender = gender
        self.api = None
        self.face_detector = None
        self.vocal_processor = None

        if quality != 'local':
            self._init_components()

    def _init_components(self):
        """Initialize lip sync components"""
        # Initialize API (FAL AI PixVerse)
        try:
            from core.lipsync_api import LipSyncAPI
            self.api = LipSyncAPI()
            print("LipSyncAPI initialized (FAL AI PixVerse)")
            logger.info("LipSyncAPI initialized")
        except Exception as e:
            print(f"Could not init LipSyncAPI: {e}")
            logger.warning(f"Could not init LipSyncAPI: {e}")

        # Initialize face detector (OpenCV - no MediaPipe!)
        try:
            from core.face_detector import FaceDetector
            self.face_detector = FaceDetector()
            logger.info("FaceDetector initialized")
        except Exception as e:
            print(f"Could not init FaceDetector: {e}")
            logger.warning(f"Could not init FaceDetector: {e}")

        # Initialize vocal processor
        try:
            from core.vocal_processor import VocalProcessor
            self.vocal_processor = VocalProcessor()
            print("VocalProcessor initialized")
            logger.info("VocalProcessor initialized")
        except Exception as e:
            print(f"Could not init VocalProcessor: {e}")
            logger.warning(f"Could not init VocalProcessor: {e}")

    def should_process(self) -> bool:
        """Check if lip sync should be processed"""
        return self.quality in ('standard', 'pro') and self.api is not None

    def detect_face_clips(self, clips_data: List[Dict]) -> List[Dict]:
        """Identify clips with faces using OpenCV"""
        if not self.face_detector:
            # FALLBACK: If face detector fails, assume ALL clips might have faces
            # FAL AI will handle clips without faces gracefully
            print("  [LIP SYNC] Face detector not available - sending all clips to FAL AI")
            logger.warning("Face detector not available - using all clips")
            return clips_data[:10]  # Limit to 10 clips max

        face_clips = []

        for clip in clips_data:
            clip_path = clip.get('path', '')
            if not clip_path or not os.path.exists(clip_path):
                continue

            try:
                result = self.face_detector.detect_faces_in_video(clip_path)
                if result.get('has_face', False):
                    clip['face_data'] = result
                    face_clips.append(clip)
                    print(f"  [FACE] Found face in: {os.path.basename(clip_path)} (conf: {result.get('confidence', 0):.0%})")
            except Exception as e:
                logger.warning(f"Face detection failed for {clip_path}: {e}")

        print(f"  [LIP SYNC] Found {len(face_clips)} clips with faces")
        logger.info(f"Found {len(face_clips)} clips with faces")
        return face_clips

    def extract_vocals(self, music_path: str) -> Optional[str]:
        """Extract vocals from music using Demucs"""
        if not self.vocal_processor:
            print("  [LIP SYNC] Vocal processor not available")
            logger.warning("Vocal processor not available")
            return None

        try:
            result = self.vocal_processor.process_audio(music_path)
            vocals_path = result.get('vocals_path')

            if vocals_path and os.path.exists(vocals_path):
                print(f"  [LIP SYNC] Extracted vocals to: {vocals_path}")
                logger.info(f"Extracted vocals to: {vocals_path}")
                return vocals_path
        except Exception as e:
            print(f"  [LIP SYNC] Vocal extraction failed: {e}")
            logger.warning(f"Vocal extraction failed: {e}")

        return None

    def process_clip(self, clip_path: str, vocals_path: str, progress_callback=None) -> Optional[str]:
        """Process single clip with FAL AI PixVerse lip sync"""
        if not self.api:
            return clip_path

        try:
            print(f"  [LIP SYNC] Processing: {os.path.basename(clip_path)}")
            
            result = self.api.sync_video(
                video_path=clip_path,
                audio_path=vocals_path,
                quality=self.quality,
                progress_callback=progress_callback
            )

            if result.success and result.output_path:
                print(f"  [LIP SYNC] ✓ Complete: {os.path.basename(clip_path)}")
                logger.info(f"Lip sync complete: {clip_path}")
                return result.output_path
            else:
                print(f"  [LIP SYNC] ✗ Failed: {result.error}")
                logger.warning(f"Lip sync failed: {result.error}")
                return clip_path
        except Exception as e:
            print(f"  [LIP SYNC] ✗ Error: {e}")
            logger.warning(f"Lip sync error: {e}")
            return clip_path

    def process_clips_batch(
        self,
        clips: List[Dict],
        vocals_path: str,
        max_clips: int = 10,
        progress_callback=None
    ) -> Dict[str, str]:
        """Process multiple clips with FAL AI PixVerse lip sync"""
        path_mapping = {}

        if not clips:
            print("  [LIP SYNC] No clips to process")
            return path_mapping

        # Sort by face confidence (highest first)
        scored = []
        for clip in clips:
            face_data = clip.get('face_data', {})
            score = face_data.get('confidence', 0.5) * 100
            scored.append((score, clip))

        scored.sort(reverse=True, key=lambda x: x[0])

        # Process top clips (limit to max_clips)
        to_process = [c[1] for c in scored[:max_clips]]
        
        print(f"  [LIP SYNC] Processing {len(to_process)} clips with FAL AI PixVerse...")

        for i, clip in enumerate(to_process):
            clip_path = clip['path']

            if progress_callback:
                pct = int((i / len(to_process)) * 100)
                progress_callback(pct, f"Lip sync {i+1}/{len(to_process)}")

            result_path = self.process_clip(clip_path, vocals_path)
            path_mapping[clip_path] = result_path

        print(f"  [LIP SYNC] Batch complete: {len(path_mapping)} clips processed")
        return path_mapping
