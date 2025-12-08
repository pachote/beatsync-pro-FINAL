"""
BeatSync PRO - Segment Quality Analyzer
Analyzes every part of every clip to find the BEST moments
This is what makes editing truly intelligent
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple
import threading
from pathlib import Path


class SegmentQualityAnalyzer:
    """Analyzes video quality at segment level - finds best parts of each clip"""
    
    def __init__(self):
        self.cache = {}
        self.cache_lock = threading.Lock()
        self.segment_duration = 0.5  # Analyze every 0.5 seconds
    
    def analyze_video_segments(self, video_path: str) -> Dict:
        """
        Analyze video quality segment by segment
        
        Returns:
        {
            'duration': 8.0,
            'segments': [
                {'start': 0.0, 'end': 0.5, 'quality': 95, 'issues': []},
                {'start': 0.5, 'end': 1.0, 'quality': 45, 'issues': ['morphing']},
                {'start': 1.0, 'end': 1.5, 'quality': 92, 'issues': []},
                ...
            ],
            'best_segments': [
                {'start': 0.0, 'end': 0.5, 'quality': 95},
                {'start': 4.5, 'end': 5.5, 'quality': 98}  # Best moment
            ],
            'skip_segments': [
                {'start': 0.5, 'end': 1.0, 'reason': 'morphing'}
            ]
        }
        """
        
        cache_key = video_path
        with self.cache_lock:
            if cache_key in self.cache:
                return self.cache[cache_key]
        
        try:
            print(f"  🔍 Quality analysis: {Path(video_path).name}")
            
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            if duration == 0:
                cap.release()
                return self._get_default_quality_data(8.0)
            
            segments = []
            current_time = 0.0
            frames_per_segment = int(fps * self.segment_duration)
            
            while current_time < duration:
                segment_end = min(current_time + self.segment_duration, duration)
                
                # Get frames for this segment
                start_frame = int(current_time * fps)
                end_frame = int(segment_end * fps)
                
                # Analyze this segment
                quality_score, issues = self._analyze_segment(
                    cap, start_frame, end_frame, fps
                )
                
                segments.append({
                    'start': round(current_time, 2),
                    'end': round(segment_end, 2),
                    'quality': quality_score,
                    'issues': issues
                })
                
                current_time = segment_end
            
            cap.release()
            
            # Identify best and worst segments
            best_segments = [s for s in segments if s['quality'] >= 85]
            skip_segments = [
                {'start': s['start'], 'end': s['end'], 'reason': s['issues'][0]}
                for s in segments if s['quality'] < 50
            ]
            
            # Sort best segments by quality
            best_segments.sort(key=lambda x: x['quality'], reverse=True)
            
            result = {
                'duration': duration,
                'segments': segments,
                'best_segments': best_segments[:5],  # Top 5 best moments
                'skip_segments': skip_segments,
                'average_quality': np.mean([s['quality'] for s in segments])
            }
            
            with self.cache_lock:
                self.cache[cache_key] = result
            
            print(f"     ✅ Quality: {result['average_quality']:.0f}/100 | Best: {len(best_segments)} | Skip: {len(skip_segments)}")
            
            return result
            
        except Exception as e:
            print(f"     ⚠️ Quality analysis error: {e}")
            return self._get_default_quality_data(8.0)
    
    def _analyze_segment(self, cap: cv2.VideoCapture, start_frame: int, 
                        end_frame: int, fps: float) -> Tuple[int, List[str]]:
        """Analyze a specific segment for quality"""
        
        issues = []
        quality_score = 100
        
        # Sample frames from this segment
        sample_frames = []
        frame_indices = np.linspace(start_frame, end_frame - 1, min(5, end_frame - start_frame), dtype=int)
        
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if ret:
                sample_frames.append(frame)
        
        if len(sample_frames) < 2:
            return 70, ['insufficient_data']
        
        # 1. CHECK FOR MORPHING/GLITCHES
        morphing_score = self._detect_morphing(sample_frames)
        if morphing_score > 0.7:
            issues.append('morphing')
            quality_score -= 40
        elif morphing_score > 0.4:
            quality_score -= 20
        
        # 2. CHECK BLUR
        blur_score = self._detect_blur(sample_frames[0])
        if blur_score < 100:
            issues.append('blurry')
            quality_score -= (100 - blur_score) // 2
        
        # 3. CHECK BRIGHTNESS/EXPOSURE
        brightness_score = self._check_brightness(sample_frames[0])
        if brightness_score < 100:
            quality_score -= (100 - brightness_score) // 3
        
        # 4. CHECK MOTION QUALITY
        motion_score = self._check_motion_quality(sample_frames)
        if motion_score > 80:  # Good motion
            quality_score += 10
        elif motion_score < 20:  # Static/boring
            quality_score -= 15
        
        # 5. CHECK ARTIFACTS
        artifact_score = self._detect_artifacts(sample_frames[0])
        if artifact_score > 0.5:
            issues.append('artifacts')
            quality_score -= 25
        
        # Clamp score
        quality_score = max(0, min(100, quality_score))
        
        return quality_score, issues
    
    def _detect_morphing(self, frames: List[np.ndarray]) -> float:
        """Detect morphing/glitching between frames"""
        if len(frames) < 2:
            return 0.0
        
        try:
            diffs = []
            for i in range(len(frames) - 1):
                # Resize for speed
                f1 = cv2.resize(frames[i], (160, 90))
                f2 = cv2.resize(frames[i + 1], (160, 90))
                
                # Convert to grayscale
                g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
                g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
                
                # Calculate difference
                diff = np.abs(g1.astype(float) - g2.astype(float)).mean()
                diffs.append(diff)
            
            # High variance = morphing/glitching
            variance = np.var(diffs)
            morphing_score = min(1.0, variance / 1000.0)
            
            return morphing_score
            
        except:
            return 0.0
    
    def _detect_blur(self, frame: np.ndarray) -> int:
        """Detect blur using Laplacian variance"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Higher variance = sharper
            # Typical values: <100 = very blurry, >500 = sharp
            if laplacian_var > 500:
                return 100
            elif laplacian_var > 200:
                return 80
            elif laplacian_var > 100:
                return 60
            else:
                return 40
                
        except:
            return 70
    
    def _check_brightness(self, frame: np.ndarray) -> int:
        """Check if brightness is good"""
        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            v = hsv[:, :, 2].mean()
            
            # Optimal brightness: 100-180
            if 100 <= v <= 180:
                return 100
            elif 80 <= v <= 200:
                return 80
            elif v < 50 or v > 220:
                return 40  # Too dark or too bright
            else:
                return 60
                
        except:
            return 70
    
    def _check_motion_quality(self, frames: List[np.ndarray]) -> int:
        """Check motion quality - too static is boring, too much is chaotic"""
        if len(frames) < 2:
            return 50
        
        try:
            motion_scores = []
            for i in range(len(frames) - 1):
                # Optical flow or simple diff
                f1 = cv2.resize(frames[i], (160, 90))
                f2 = cv2.resize(frames[i + 1], (160, 90))
                
                g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
                g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
                
                diff = np.abs(g1.astype(float) - g2.astype(float)).mean()
                motion_scores.append(diff)
            
            avg_motion = np.mean(motion_scores)
            
            # Good motion: 5-30
            if 5 <= avg_motion <= 30:
                return 90
            elif avg_motion < 5:
                return 30  # Too static
            elif avg_motion > 50:
                return 40  # Too chaotic
            else:
                return 60
                
        except:
            return 50
    
    def _detect_artifacts(self, frame: np.ndarray) -> float:
        """Detect compression artifacts"""
        try:
            # Simple artifact detection using edge detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            # Too many edges in wrong places = artifacts
            edge_density = edges.mean() / 255.0
            
            if edge_density > 0.3:
                return 0.8  # Likely artifacts
            elif edge_density > 0.2:
                return 0.4
            else:
                return 0.0
                
        except:
            return 0.0
    
    def _get_default_quality_data(self, duration: float) -> Dict:
        """Fallback data"""
        num_segments = int(duration / self.segment_duration)
        segments = [
            {
                'start': i * self.segment_duration,
                'end': (i + 1) * self.segment_duration,
                'quality': 70,
                'issues': []
            }
            for i in range(num_segments)
        ]
        
        return {
            'duration': duration,
            'segments': segments,
            'best_segments': segments[:3],
            'skip_segments': [],
            'average_quality': 70
        }


# Global instance
segment_quality_analyzer = SegmentQualityAnalyzer()
