"""
BeatSync PRO - Quality & Segment Analyzer
Detects best parts of clips, scores quality, identifies glitches/morphing
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import threading


class QualityAnalyzer:
    """Analyzes video quality and identifies best segments to use"""
    
    def __init__(self):
        self.cache = {}
        self.cache_lock = threading.Lock()
    
    def analyze_clip_quality(self, video_path: str, segment_duration: float = 2.0) -> Dict:
        """
        Analyze video quality and identify best segments
        
        Returns:
        {
            'segments': [{'start': 0.0, 'end': 2.0, 'quality_score': 8.5, ...}],
            'best_segments': [(start, end, score), ...],
            'bad_segments': [(start, end, reason), ...],
            'recommended_usage': {'intro': (0, 2), 'climax': (4, 7)}
        }
        """
        
        cache_key = f"{video_path}_{Path(video_path).stat().st_mtime}"
        with self.cache_lock:
            if cache_key in self.cache:
                return self.cache[cache_key]
        
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return self._get_default_quality_data()
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if fps == 0 or frame_count == 0:
                cap.release()
                return self._get_default_quality_data()
            
            duration = frame_count / fps
            
            # Analyze in segments
            segments = []
            segment_frames = int(segment_duration * fps)
            
            frame_idx = 0
            prev_frame = None
            segment_data = {'motion_scores': [], 'sharpness_scores': [], 'stability_scores': []}
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Analyze every 5th frame for speed
                if frame_idx % 5 == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray_small = cv2.resize(gray, (320, 180))
                    
                    # Calculate sharpness
                    laplacian = cv2.Laplacian(gray_small, cv2.CV_64F)
                    sharpness = laplacian.var() / 1000.0
                    segment_data['sharpness_scores'].append(min(sharpness, 1.0))
                    
                    # Calculate motion
                    if prev_frame is not None:
                        diff = cv2.absdiff(gray_small, prev_frame)
                        motion = np.mean(diff) / 255.0
                        segment_data['motion_scores'].append(motion)
                        
                        # Detect instability
                        if len(segment_data['motion_scores']) > 2:
                            recent_motion = segment_data['motion_scores'][-3:]
                            stability = 1.0 - np.std(recent_motion)
                            segment_data['stability_scores'].append(max(0, stability))
                    
                    prev_frame = gray_small
                
                # End of segment?
                if (frame_idx + 1) % segment_frames == 0 or frame_idx == frame_count - 1:
                    segment_start = len(segments) * segment_duration
                    segment_end = min(segment_start + segment_duration, duration)
                    
                    # Calculate scores
                    avg_motion = np.mean(segment_data['motion_scores']) if segment_data['motion_scores'] else 0.5
                    avg_sharpness = np.mean(segment_data['sharpness_scores']) if segment_data['sharpness_scores'] else 0.5
                    avg_stability = np.mean(segment_data['stability_scores']) if segment_data['stability_scores'] else 0.8
                    
                    quality_score = (avg_sharpness * 5 + avg_stability * 5)
                    has_issues = avg_stability < 0.5 or avg_sharpness < 0.3
                    
                    # Find best moment
                    if segment_data['motion_scores']:
                        peak_idx = np.argmax(segment_data['motion_scores'])
                        best_moment = segment_start + (peak_idx * 5 / fps)
                    else:
                        best_moment = segment_start + segment_duration / 2
                    
                    overall_score = int((quality_score * 7 + avg_motion * 10 * 3) / 10 * 100)
                    
                    segment_info = {
                        'start': round(segment_start, 2),
                        'end': round(segment_end, 2),
                        'quality_score': round(quality_score, 1),
                        'motion_score': round(avg_motion, 2),
                        'has_issues': has_issues,
                        'best_moment': round(best_moment, 2),
                        'overall_score': overall_score
                    }
                    
                    segments.append(segment_info)
                    segment_data = {'motion_scores': [], 'sharpness_scores': [], 'stability_scores': []}
                
                frame_idx += 1
            
            cap.release()
            
            if not segments:
                return self._get_default_quality_data()
            
            # Identify best and bad segments
            best_segments = sorted(
                [(s['start'], s['end'], s['overall_score']) for s in segments if not s['has_issues']],
                key=lambda x: x[2], reverse=True
            )[:3]
            
            bad_segments = [(s['start'], s['end'], 'quality_issues') for s in segments if s['has_issues']]
            
            # Recommend usage
            recommended = {}
            high_energy = sorted(segments, key=lambda s: s['motion_score'], reverse=True)
            if high_energy and high_energy[0]['overall_score'] > 70:
                s = high_energy[0]
                recommended['climax'] = (s['start'], s['end'])
            
            result = {
                'segments': segments,
                'best_segments': best_segments,
                'bad_segments': bad_segments,
                'recommended_usage': recommended,
                'total_duration': round(duration, 2)
            }
            
            with self.cache_lock:
                self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            return self._get_default_quality_data()
    
    def _get_default_quality_data(self) -> Dict:
        """Default data when analysis fails"""
        return {
            'segments': [{'start': 0.0, 'end': 8.0, 'quality_score': 7.0, 'motion_score': 0.5, 
                         'has_issues': False, 'best_moment': 4.0, 'overall_score': 75}],
            'best_segments': [(0.0, 8.0, 75)],
            'bad_segments': [],
            'recommended_usage': {'intro': (0, 8)},
            'total_duration': 8.0
        }


# Global instance
quality_analyzer = QualityAnalyzer()
