"""
BeatSync PRO - Smart Clip Trimming Engine
Claude AI selects the BEST moment in each clip
Not just the middle - intelligent frame selection
"""

from typing import Dict, Tuple
import random


class SmartTrimmingEngine:
    """
    AI-powered clip trimming engine
    Selects optimal start point based on:
    - Content type (face, action, scenery)
    - Desired clip duration
    - Video analysis data
    """
    
    def __init__(self):
        self.trimming_history = []
    
    def select_trim_point(self,
                         clip_data: Dict,
                         desired_duration: float,
                         music_energy: float = 0.5,
                         previous_clip: Dict = None) -> Dict:
        """
        Intelligently select where to trim the clip
        
        Args:
            clip_data: Full clip data with analysis
            desired_duration: How long the clip should be
            music_energy: Current music energy (affects selection)
            previous_clip: Previous clip data (for variety)
        
        Returns:
            Dict with trim_start, duration, and reasoning
        """
        
        # Get clip analysis
        analysis = clip_data.get('analysis', {})
        video_path = clip_data.get('video_path', '')
        
        # Get source duration (assume 5 seconds for Kling videos)
        source_duration = clip_data.get('source_duration', 5.0)
        
        # Extract analysis attributes
        subject_type = analysis.get('subject', 'unknown')
        has_face = 'human' in subject_type.lower() or 'character' in subject_type.lower()
        energy_level = analysis.get('energy', 5)
        is_lip_sync = analysis.get('lip_sync_suitable', False)
        
        # Determine optimal trim strategy
        strategy = self._determine_trim_strategy(
            has_face=has_face,
            energy_level=energy_level,
            is_lip_sync=is_lip_sync,
            music_energy=music_energy,
            source_duration=source_duration,
            desired_duration=desired_duration
        )
        
        # Calculate trim point based on strategy
        trim_point = self._calculate_trim_point(
            strategy=strategy,
            source_duration=source_duration,
            desired_duration=desired_duration,
            previous_clip=previous_clip
        )
        
        # Track history
        self.trimming_history.append(strategy)
        
        return {
            'trim_start': trim_point,
            'duration': desired_duration,
            'strategy': strategy['name'],
            'reasoning': strategy['reasoning']
        }
    
    def _determine_trim_strategy(self,
                                 has_face: bool,
                                 energy_level: int,
                                 is_lip_sync: bool,
                                 music_energy: float,
                                 source_duration: float,
                                 desired_duration: float) -> Dict:
        """Determine which trimming strategy to use"""
        
        # STRATEGY 1: FACE-CENTERED (for face shots)
        if has_face and is_lip_sync:
            return {
                'name': 'face_centered',
                'position': 0.4,  # Slightly before middle (face reveal)
                'reasoning': 'Face-centered for lip sync potential'
            }
        
        # STRATEGY 2: ACTION PEAK (for high energy)
        elif energy_level >= 7 or music_energy > 0.7:
            return {
                'name': 'action_peak',
                'position': 0.6,  # After middle (peak action)
                'reasoning': 'Peak action moment'
            }
        
        # STRATEGY 3: EARLY START (for scene establishment)
        elif energy_level <= 3 or music_energy < 0.3:
            return {
                'name': 'early_start',
                'position': 0.2,  # Early (scene establishment)
                'reasoning': 'Scene establishment'
            }
        
        # STRATEGY 4: LATE CLIMAX (for dramatic moments)
        elif music_energy > 0.8:
            return {
                'name': 'late_climax',
                'position': 0.75,  # Late (climax moment)
                'reasoning': 'Climax moment'
            }
        
        # STRATEGY 5: RANDOM VARIETY (prevent repetition)
        elif random.random() < 0.15:  # 15% of clips
            position = random.uniform(0.2, 0.8)
            return {
                'name': 'variety',
                'position': position,
                'reasoning': 'Variety to prevent repetition'
            }
        
        # STRATEGY 6: MIDDLE (default fallback)
        else:
            return {
                'name': 'middle',
                'position': 0.5,
                'reasoning': 'Balanced middle section'
            }
    
    def _calculate_trim_point(self,
                              strategy: Dict,
                              source_duration: float,
                              desired_duration: float,
                              previous_clip: Dict = None) -> float:
        """Calculate actual trim start time"""
        
        position = strategy['position']
        
        # Adjust for desired duration
        # If desired duration is short, we have more flexibility
        # If desired duration is long, we need to be closer to start
        
        max_start = max(0, source_duration - desired_duration)
        
        # Calculate ideal start point
        ideal_start = position * max_start
        
        # Add small random variation (±10%)
        variation = random.uniform(-0.1, 0.1) * max_start
        trim_start = ideal_start + variation
        
        # Clamp to valid range
        trim_start = max(0, min(trim_start, max_start))
        
        # Avoid same trim point as previous clip (if clips are identical)
        if previous_clip:
            prev_trim = previous_clip.get('trim_start', 0)
            prev_path = previous_clip.get('video_path', '')
            curr_path = previous_clip.get('video_path', '')  # Would come from parent
            
            if prev_path == curr_path and abs(trim_start - prev_trim) < 0.3:
                # Too similar, adjust
                if max_start > 0:
                    trim_start = (trim_start + 1.0) % max_start if max_start > 0 else 0 if max_start > 0 else 0
                else:
                    trim_start = 0  # Clip too short, use start
        
        return round(float(trim_start), 3)
    
    def get_statistics(self) -> Dict:
        """Get trimming strategy usage statistics"""
        total = len(self.trimming_history)
        if total == 0:
            return {}
        
        strategies = {}
        for strategy in self.trimming_history:
            name = strategy['name']
            strategies[name] = strategies.get(name, 0) + 1
        
        stats = {}
        for name, count in strategies.items():
            stats[name] = {
                'count': count,
                'percentage': (count / total) * 100
            }
        
        return stats


class ContentAnalyzer:
    """
    Enhanced content analysis for clip trimming
    Works with Claude's video analysis results
    """
    
    @staticmethod
    def analyze_clip_for_trimming(analysis: Dict) -> Dict:
        """
        Extract trimming-relevant info from Claude analysis
        
        Args:
            analysis: Claude video analysis results
        
        Returns:
            Dict with trimming recommendations
        """
        
        subject = analysis.get('subject', 'unknown').lower()
        energy = analysis.get('energy', 5)
        style = analysis.get('art_style', 'unknown').lower()
        
        # Determine content characteristics
        has_face = 'human' in subject or 'character' in subject
        is_action = energy >= 6
        is_calm = energy <= 4
        is_artistic = any(word in style for word in ['anime', 'illustration', 'digital', 'abstract'])
        
        return {
            'has_face': has_face,
            'is_action': is_action,
            'is_calm': is_calm,
            'is_artistic': is_artistic,
            'subject_type': subject,
            'energy_level': energy
        }




