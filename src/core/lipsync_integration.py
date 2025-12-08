"""
BeatSync PRO - Lip Sync Integration Layer (TIMELINE-AWARE)
Connects vocal separation and FAL AI PixVerse lip sync API
Each clip syncs to its EXACT timeline position - not the full song!
"""

import os
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, List
import shutil

logger = logging.getLogger(__name__)


class LipSyncIntegration:
    """Integrates lip sync into video rendering pipeline"""

    def __init__(self, quality: str = 'local', gender: str = 'female'):
        self.quality = quality
        self.gender = gender
        self.api = None
        self.face_detector = None
        self.vocal_processor = None
        self.temp_dir = Path(tempfile.gettempdir()) / '.beatsync' / 'lipsync_segments'
        self.temp_dir.mkdir(parents=True, exist_ok=True)

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

    def _extract_audio_segment(self, vocals_path: str, start_time: float, end_time: float, clip_index: int) -> Optional[str]:
        """Extract specific audio segment using FFmpeg for timeline-accurate lip sync"""
        try:
            duration = end_time - start_time
            output_path = self.temp_dir / f"segment_{clip_index}_{start_time:.2f}_{end_time:.2f}.wav"
            
            # Skip if segment already exists and is valid
            if output_path.exists() and output_path.stat().st_size > 1000:
                return str(output_path)
            
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(start_time),
                '-t', str(duration),
                '-i', vocals_path,
                '-acodec', 'pcm_s16le',
                '-ar', '44100',
                '-ac', '1',  # Mono for lip sync
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and output_path.exists():
                print(f"    [SEGMENT] Extracted {start_time:.2f}s-{end_time:.2f}s ({duration:.2f}s)")
                return str(output_path)
            else:
                logger.warning(f"FFmpeg segment extraction failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.warning(f"Audio segment extraction failed: {e}")
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
                print(f"  [LIP SYNC] ? Complete: {os.path.basename(clip_path)}")
                logger.info(f"Lip sync complete: {clip_path}")
                return result.output_path
            else:
                print(f"  [LIP SYNC] ? Failed: {result.error}")
                logger.warning(f"Lip sync failed: {result.error}")
                return clip_path
        except Exception as e:
            print(f"  [LIP SYNC] ? Error: {e}")
            logger.warning(f"Lip sync error: {e}")
            return clip_path

    def process_clips_batch(
        self,
        clips: List[Dict],
        vocals_path: str,
        max_clips: int = 10,
        progress_callback=None
    ) -> Dict[str, str]:
        """Process multiple clips with FAL AI PixVerse lip sync (LEGACY - full audio)"""
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

    # ==========================================================================
    # TIMELINE-AWARE LIP SYNC (THE MAGIC!)
    # ==========================================================================
    
    def process_clips_with_timeline(
        self,
        edit_plan: List[Dict],
        vocals_path: str,
        max_clips: int = 10,
        progress_callback=None
    ) -> Dict[str, str]:
        """
        ADVANCED: Process clips with TIMELINE-ACCURATE lip sync!
        
        Each clip gets synced to ONLY the audio segment it will play over,
        not the full song. This ensures lip movements match the actual
        vocal position in the final edited video.
        
        Args:
            edit_plan: List of clip dicts with 'video_path', 'start_time', 'end_time'
            vocals_path: Path to extracted vocals (full track)
            max_clips: Maximum clips to process (API cost control)
            progress_callback: Progress reporting function
            
        Returns:
            Dict mapping original video_path -> lip_synced_path
        """
        path_mapping = {}
        
        if not edit_plan:
            print("  [LIP SYNC] No edit plan provided")
            return path_mapping
            
        if not self.api:
            print("  [LIP SYNC] API not available")
            return path_mapping
            
        print(f"\n{'='*60}")
        print(f"  [LIP SYNC] TIMELINE-AWARE MODE ACTIVATED")
        print(f"  [LIP SYNC] Processing {len(edit_plan)} clips in edit plan")
        print(f"{'='*60}\n")
        
        # Step 1: Identify clips with faces from edit_plan
        face_clips_with_timeline = []
        
        for i, clip in enumerate(edit_plan):
            video_path = clip.get('video_path', '')
            start_time = clip.get('start_time', 0)
            end_time = clip.get('end_time', 0)
            
            if not video_path or not os.path.exists(video_path):
                continue
                
            # Check for face
            has_face = False
            confidence = 0.5
            
            if self.face_detector:
                try:
                    result = self.face_detector.detect_faces_in_video(video_path)
                    has_face = result.get('has_face', False)
                    confidence = result.get('confidence', 0.5)
                except Exception as e:
                    logger.warning(f"Face detection failed: {e}")
                    has_face = True  # Assume face on error
                    confidence = 0.3
            else:
                # No face detector - assume all clips might have faces
                has_face = True
                confidence = 0.5
                
            if has_face:
                face_clips_with_timeline.append({
                    'video_path': video_path,
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': end_time - start_time,
                    'confidence': confidence,
                    'edit_index': i
                })
                print(f"  [FACE] Clip {i}: {os.path.basename(video_path)} @ {start_time:.2f}s-{end_time:.2f}s (conf: {confidence:.0%})")
        
        print(f"\n  [LIP SYNC] Found {len(face_clips_with_timeline)} face clips in timeline")
        
        if not face_clips_with_timeline:
            print("  [LIP SYNC] No face clips detected")
            return path_mapping
            
        # Step 2: Sort by confidence and limit
        face_clips_with_timeline.sort(key=lambda x: x['confidence'], reverse=True)
        to_process = face_clips_with_timeline[:max_clips]
        
        print(f"  [LIP SYNC] Processing top {len(to_process)} clips by confidence\n")
        
        # Step 3: Process each clip with its SPECIFIC audio segment
        processed_count = 0
        failed_count = 0
        
        for i, clip_info in enumerate(to_process):
            video_path = clip_info['video_path']
            start_time = clip_info['start_time']
            end_time = clip_info['end_time']
            edit_idx = clip_info['edit_index']
            
            if progress_callback:
                pct = int((i / len(to_process)) * 100)
                progress_callback(pct, f"Timeline lip sync {i+1}/{len(to_process)}")
            
            print(f"\n  [{i+1}/{len(to_process)}] Processing clip at timeline {start_time:.2f}s-{end_time:.2f}s")
            print(f"      Video: {os.path.basename(video_path)}")
            
            # Extract the specific audio segment for this clip's timeline position
            segment_path = self._extract_audio_segment(vocals_path, start_time, end_time, edit_idx)
            
            if not segment_path:
                print(f"      ? Audio segment extraction failed")
                failed_count += 1
                continue
                
            print(f"      Audio: {os.path.basename(segment_path)}")
            
            # Send to FAL AI with the SPECIFIC audio segment
            try:
                result = self.api.sync_video(
                    video_path=video_path,
                    audio_path=segment_path,
                    quality=self.quality,
                    progress_callback=None
                )
                
                if result.success and result.output_path:
                    path_mapping[edit_idx] = result.output_path
                    processed_count += 1
                    print(f"      ? Lip sync complete!")
                    print(f"      Output: {os.path.basename(result.output_path)}")
                else:
                    print(f"      ? Lip sync failed: {result.error}")
                    failed_count += 1
                    
            except Exception as e:
                print(f"      ? Error: {e}")
                failed_count += 1
                logger.warning(f"Timeline lip sync error: {e}")
        
        print(f"\n{'='*60}")
        print(f"  [LIP SYNC] TIMELINE SYNC COMPLETE")
        print(f"  [LIP SYNC] ? Processed: {processed_count}")
        print(f"  [LIP SYNC] ? Failed: {failed_count}")
        print(f"  [LIP SYNC] Total mappings: {len(path_mapping)}")
        print(f"{'='*60}\n")
        
        return path_mapping
        
    def cleanup_temp_segments(self):
        """Clean up temporary audio segment files"""
        try:
            if self.temp_dir.exists():
                for f in self.temp_dir.glob("segment_*.wav"):
                    f.unlink()
                print("  [LIP SYNC] Cleaned up temp audio segments")
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")
