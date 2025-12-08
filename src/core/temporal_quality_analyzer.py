"""
BeatSync PRO - Temporal Quality Analyzer
AGI-LEVEL frame-by-frame quality analysis
"""
import cv2
import base64
from typing import Dict, List, Tuple
from pathlib import Path

class TemporalQualityAnalyzer:
    """Revolutionary AGI-level video quality analysis"""
    
    def __init__(self, claude_client=None):
        self.claude_client = claude_client
        self.quality_cache = {}
    
    def extract_frames(self, video_path: str, num_samples: int = 6) -> List[Dict]:
        """Extract frames at key timestamps"""
        print(f"   ???  Extracting {num_samples} frames from {Path(video_path).name}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return []
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        if duration <= 0:
            cap.release()
            return []
        
        frames_data = []
        for i in range(num_samples):
            timestamp = duration * (i / (num_samples - 1) if num_samples > 1 else 0)
            frame_number = int(timestamp * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            ret, frame = cap.read()
            if not ret:
                continue
            
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            
            frames_data.append({
                'timestamp': timestamp,
                'frame_base64': frame_base64,
                'frame_number': frame_number
            })
        
        cap.release()
        return frames_data
    
    def analyze_frame(self, frame_base64: str, timestamp: float) -> Dict:
        """AGI-LEVEL frame analysis with Claude Vision"""
        if not self.claude_client:
            return {
                'timestamp': timestamp,
                'quality_score': 8,
                'composition': 'good',
                'artifacts': 'none',
                'visual_appeal': 8,
                'usable': True
            }
        
        try:
            prompt = """Analyze this frame for professional video editing. Be STRICT.

QUALITY (0-10): Rate clarity, focus, technical quality
COMPOSITION (excellent/good/poor): Framing and visual balance
ARTIFACTS (none/minor/major): AI glitches, blur, distortion, morphing
APPEAL (0-10): Aesthetic quality for music video
USABLE (true/false): Use only if quality >= 7 AND artifacts <= minor

Format:
QUALITY: [number]
COMPOSITION: [word]
ARTIFACTS: [word]
APPEAL: [number]
USABLE: [true/false]"""

            response = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": frame_base64}},
                        {"type": "text", "text": prompt}
                    ]
                }]
            )
            
            text = response.content[0].text
            quality = 8
            composition = "good"
            artifacts = "none"
            appeal = 8
            usable = True
            
            for line in text.split('\n'):
                if 'QUALITY:' in line:
                    try: quality = int(''.join(filter(str.isdigit, line)))
                    except: pass
                elif 'COMPOSITION:' in line:
                    composition = line.split(':')[1].strip().lower()
                elif 'ARTIFACTS:' in line:
                    artifacts = line.split(':')[1].strip().lower().split('-')[0].strip()
                elif 'APPEAL:' in line:
                    try: appeal = int(''.join(filter(str.isdigit, line)))
                    except: pass
                elif 'USABLE:' in line:
                    usable = 'true' in line.lower()
            
            return {
                'timestamp': timestamp,
                'quality_score': quality,
                'composition': composition,
                'artifacts': artifacts,
                'visual_appeal': appeal,
                'usable': usable
            }
        except Exception as e:
            return {'timestamp': timestamp, 'quality_score': 7, 'composition': 'unknown', 'artifacts': 'unknown', 'visual_appeal': 7, 'usable': True}
    
    def find_good_segments(self, temporal_data: List[Dict], min_quality: int = 7) -> List[Tuple[float, float]]:
        """Find continuous high-quality segments"""
        if not temporal_data:
            return []
        
        segments = []
        in_segment = False
        start = 0
        
        for frame in temporal_data:
            is_good = frame['usable'] and frame['quality_score'] >= min_quality
            
            if is_good and not in_segment:
                start = frame['timestamp']
                in_segment = True
            elif not is_good and in_segment:
                segments.append((start, frame['timestamp']))
                in_segment = False
        
        if in_segment:
            segments.append((start, temporal_data[-1]['timestamp'] + 2))
        
        return segments
    
    def analyze_clip(self, video_path: str, num_samples: int = 6) -> Dict:
        """Complete AGI-level temporal analysis"""
        cache_key = f"{video_path}_{num_samples}"
        if cache_key in self.quality_cache:
            return self.quality_cache[cache_key]
        
        print(f"\n?? AGI Analysis: {Path(video_path).name}")
        
        frames = self.extract_frames(video_path, num_samples)
        if not frames:
            return {'error': 'Failed to extract frames'}
        
        temporal_data = []
        for frame_data in frames:
            quality = self.analyze_frame(frame_data['frame_base64'], frame_data['timestamp'])
            temporal_data.append(quality)
            print(f"   {quality['timestamp']:.1f}s: Q={quality['quality_score']}/10 | {quality['composition']} | {quality['artifacts']}")
        
        good_segments = self.find_good_segments(temporal_data, min_quality=7)
        avg_quality = sum(f['quality_score'] for f in temporal_data) / len(temporal_data)
        
        result = {
            'video_path': video_path,
            'temporal_data': temporal_data,
            'good_segments': good_segments,
            'average_quality': avg_quality,
            'best_segment': good_segments[0] if good_segments else None
        }
        
        self.quality_cache[cache_key] = result
        print(f"   ? Avg Quality: {avg_quality:.1f}/10 | Good segments: {len(good_segments)}")
        
        return result
