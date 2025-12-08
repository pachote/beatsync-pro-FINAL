"""
BeatSync PRO - Motion Analysis Engine
Detects motion peaks, action moments, and best segments in video clips
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import threading


class MotionAnalyzer:
    """Analyzes motion in video clips to find action peaks"""
    
    def __init__(self):
        self.cache = {}
        self.cache_lock = threading.Lock()
    
    def analyze_clip_motion(self, video_path: str) -> Dict:
        """
        Analyze motion in a video clip
        
        Returns:
        {
            'motion_peaks': [(timestamp, intensity), ...],
            'best_segments': [(start, end, score), ...],
            'overall_intensity': 0.0-1.0,
            'peak_timestamp': 2.34
        }
        """
        
        cache_key = f"{video_path}_{Path(video_path).stat().st_mtime}"
        with self.cache_lock:
            if cache_key in self.cache:
                return self.cache[cache_key]
        
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return self._get_default_motion_data()
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if fps == 0 or frame_count == 0:
                cap.release()
                return self._get_default_motion_data()
            
            duration = frame_count / fps
            
            # Analyze motion by sampling frames
            motion_scores = []
            prev_frame = None
            sample_rate = max(1, int(fps / 5))  # 5 samples per second
            
            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_idx % sample_rate == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray = cv2.resize(gray, (320, 180))
                    
                    if prev_frame is not None:
                        diff = cv2.absdiff(gray, prev_frame)
                        motion_score = np.mean(diff) / 255.0
                        timestamp = frame_idx / fps
                        motion_scores.append((timestamp, motion_score))
                    
                    prev_frame = gray
                
                frame_idx += 1
            
            cap.release()
            
            if not motion_scores:
                return self._get_default_motion_data()
            
            motion_peaks = self._find_peaks(motion_scores)
            best_segments = self._find_best_segments(motion_scores, duration)
            overall_intensity = np.mean([score for _, score in motion_scores])
            peak_timestamp = max(motion_scores, key=lambda x: x[1])[0]
            
            result = {
                'motion_peaks': motion_peaks[:10],
                'best_segments': best_segments[:5],
                'overall_intensity': float(overall_intensity),
                'peak_timestamp': float(peak_timestamp),
                'duration': float(duration)
            }
            
            with self.cache_lock:
                self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            print(f"  [MOTION ERROR] {Path(video_path).name}: {e}")
            return self._get_default_motion_data()
    
    def _find_peaks(self, motion_scores: List[Tuple[float, float]], threshold_percentile: float = 75) -> List[Tuple[float, float]]:
        """Find local motion peaks"""
        if len(motion_scores) < 3:
            return motion_scores
        
        scores = np.array([s for _, s in motion_scores])
        threshold = np.percentile(scores, threshold_percentile)
        
        peaks = []
        for i in range(1, len(motion_scores) - 1):
            timestamp, score = motion_scores[i]
            
            if score > threshold:
                if score > motion_scores[i-1][1] and score > motion_scores[i+1][1]:
                    peaks.append((timestamp, score))
        
        peaks.sort(key=lambda x: x[1], reverse=True)
        return peaks
    
    def _find_best_segments(self, motion_scores: List[Tuple[float, float]], duration: float, segment_length: float = 2.0) -> List[Tuple[float, float, float]]:
        """Find segments with sustained high motion"""
        if len(motion_scores) < 10:
            return [(0.0, min(duration, segment_length), 0.5)]
        
        segments = []
        window_size = int(segment_length * 5)
        
        for i in range(0, len(motion_scores) - window_size, window_size // 2):
            window = motion_scores[i:i + window_size]
            avg_score = np.mean([s for _, s in window])
            start_time = window[0][0]
            end_time = min(window[-1][0], duration)
            segments.append((start_time, end_time, avg_score))
        
        segments.sort(key=lambda x: x[2], reverse=True)
        return segments
    
    def _get_default_motion_data(self) -> Dict:
        """Default data when analysis fails"""
        return {
            'motion_peaks': [(1.0, 0.5)],
            'best_segments': [(0.0, 2.0, 0.5)],
            'overall_intensity': 0.5,
            'peak_timestamp': 1.0,
            'duration': 8.0
        }
    
    def find_best_cut_point(self, video_path: str, desired_time: float, beat_time: float, window: float = 0.5) -> float:
        """
        Find best cut point near desired time that syncs with motion peak + beat
        
        Args:
            video_path: Path to video file
            desired_time: Approximate time we want to cut
            beat_time: When the beat hits
            window: Search window around desired time (seconds)
        
        Returns:
            Optimal cut timestamp
        """
        motion_data = self.analyze_clip_motion(video_path)
        motion_peaks = motion_data['motion_peaks']
        
        if not motion_peaks:
            return beat_time
        
        # Find motion peak closest to beat within window
        candidates = [
            (peak_time, abs(peak_time - beat_time))
            for peak_time, _ in motion_peaks
            if abs(peak_time - desired_time) <= window
        ]
        
        if candidates:
            # Return peak closest to beat
            best_peak = min(candidates, key=lambda x: x[1])
            return best_peak[0]
        else:
            # No peaks in window, use beat time
            return beat_time


# Global instance
motion_analyzer = MotionAnalyzer()
