"""
BeatSync PRO - Visual Intelligence System
Powered by Claude API for accurate video content analysis
"""

import anthropic
import cv2
import base64
import json
import os
from pathlib import Path
import numpy as np
from PIL import Image
import io

# Import config
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import CLAUDE_API_KEY, FRAMES_PER_VIDEO, MAX_TOKENS


class VisualIntelligence:
    """Claude-powered video analysis engine"""
    
    def __init__(self, api_key=None):
        """Initialize with Claude API"""
        self.api_key = api_key or CLAUDE_API_KEY
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.cache = {}
    
    def analyze_video(self, video_path):
        """
        Analyze a video file using Claude's vision capabilities
        
        Args:
            video_path: Path to video file
            
        Returns:
            dict: Complete analysis with categorization data
        """
        # Check cache
        cache_key = f"{video_path}_{os.path.getmtime(video_path)}"
        if cache_key in self.cache:
            print(f"  [CACHE] {Path(video_path).name}")
            return self.cache[cache_key]
        
        print(f"  [CLAUDE AI] Analyzing {Path(video_path).name}...")
        
        try:
            # Extract frames
            frames = self._extract_key_frames(video_path, n=FRAMES_PER_VIDEO)
            
            if not frames:
                print(f"  [ERROR] Could not extract frames")
                return self._get_default_analysis()
            
            # Get technical metadata
            technical = self._get_technical_metadata(video_path)
            
            # Analyze with Claude
            semantic = self._analyze_with_claude(frames)
            
            # Combine results
            result = {
                **technical,
                **semantic,
                'filename': Path(video_path).name
            }
            
            # Cache it
            self.cache[cache_key] = result
            
            # Print summary
            print(f"  -> {result.get('content_type', '?')} | {result.get('mood', '?')} | Energy: {result.get('energy_level', 0)}/10")
            
            return result
            
        except Exception as e:
            print(f"  [ERROR] {e}")
            return self._get_default_analysis()
    
    def _extract_key_frames(self, video_path, n=6):
        """Extract N evenly-spaced frames from video"""
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return []
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if total_frames == 0:
                return []
            
            # Calculate frame indices
            indices = np.linspace(0, total_frames - 1, n, dtype=int)
            
            frames = []
            for idx in indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                
                if ret:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Resize if needed (max 1024px)
                    height, width = frame_rgb.shape[:2]
                    max_dim = 1024
                    
                    if max(height, width) > max_dim:
                        scale = max_dim / max(height, width)
                        new_width = int(width * scale)
                        new_height = int(height * scale)
                        frame_rgb = cv2.resize(frame_rgb, (new_width, new_height))
                    
                    frames.append(frame_rgb)
            
            cap.release()
            return frames
            
        except Exception as e:
            print(f"  [ERROR] Frame extraction: {e}")
            return []
    
    def _encode_frame_to_base64(self, frame):
        """Convert numpy array to base64 JPEG"""
        pil_image = Image.fromarray(frame)
        buffer = io.BytesIO()
        pil_image.save(buffer, format='JPEG', quality=85)
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')
    
    def _analyze_with_claude(self, frames):
        """Send frames to Claude for analysis"""
        
        # Build prompt
        content = [
            {
                "type": "text",
                "text": '''Analyze these video frames for music video editing. Return ONLY valid JSON (no markdown):

{
    "content_type": "",
    "visual_style": "",
    "mood": "",
    "primary_subjects": [],
    "color_palette": [],
    "color_temperature": "",
    "energy_level": 5,
    "motion_intensity": "",
    "best_use": "",
    "editing_tags": [],
    "atmosphere": ""
}

Fill in based on frames:
- content_type: person/abstract/nature/urban/vfx/mixed
- visual_style: cinematic/psychedelic/minimal/chaotic/retro/futuristic/artistic
- mood: energetic/calm/dark/vibrant/mysterious/intense/dreamy/aggressive
- color_palette: ["color1", "color2", "color3"]
- color_temperature: warm/cool/neon/neutral/mixed
- energy_level: 1-10 (rate the visual energy)
- motion_intensity: static/slow/moderate/fast/chaotic
- best_use: intro/verse/buildup/chorus/breakdown/outro
- editing_tags: ["tag1", "tag2", "tag3"]
- atmosphere: one sentence describing the vibe'''
            }
        ]
        
        # Add frames as images
        for frame in frames:
            encoded = self._encode_frame_to_base64(frame)
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": encoded
                }
            })
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=MAX_TOKENS,
                messages=[{
                    "role": "user",
                    "content": content
                }]
            )
            
            # Parse response
            response_text = response.content[0].text.strip()
            
            # Remove markdown if present
            if response_text.startswith('```'):
                # Extract JSON from markdown code block
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            # Parse JSON
            analysis = json.loads(response_text)
            
            return analysis
            
        except Exception as e:
            print(f"  [CLAUDE ERROR] {e}")
            return {}
    
    def _get_technical_metadata(self, video_path):
        """Extract basic video metadata"""
        try:
            cap = cv2.VideoCapture(video_path)
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                'resolution': f"{width}x{height}",
                'fps': round(fps, 2),
                'duration': round(duration, 2),
                'frame_count': frame_count
            }
            
        except:
            return {
                'resolution': 'unknown',
                'fps': 0,
                'duration': 0,
                'frame_count': 0
            }
    
    def _get_default_analysis(self):
        """Return default values when analysis fails"""
        return {
            'content_type': 'unknown',
            'visual_style': 'unknown',
            'mood': 'neutral',
            'primary_subjects': [],
            'color_palette': [],
            'color_temperature': 'neutral',
            'energy_level': 5,
            'motion_intensity': 'moderate',
            'best_use': 'verse',
            'editing_tags': ['uncategorized'],
            'atmosphere': 'Analysis failed',
            'resolution': 'unknown',
            'fps': 0,
            'duration': 0
        }