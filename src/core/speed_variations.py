"""
BeatSync PRO - Speed Variations Engine
Dynamic speed changes matched to music energy
Makes coordination IMPOSSIBLE for humans
"""

from typing import Dict
import random


class SpeedVariationEngine:
    """
    AI-powered speed variation engine
    Matches clip speed to music energy and content
    """
    
    # Speed presets
    SPEED_ULTRA_SLOW = 0.5      # Dramatic slow-mo
    SPEED_SLOW = 0.75           # Subtle slow-mo
    SPEED_NORMAL = 1.0          # Regular speed
    SPEED_FAST = 1.25           # Slight speed up
    SPEED_VERY_FAST = 1.5       # Energetic
    SPEED_ULTRA_FAST = 2.0      # Drop/climax
    
    def __init__(self):
        self.speed_history = []
        self.last_slow_index = -10  # Prevent slow-mo spam
        
        # Speed distribution (professional music video standard)
        self.base_weights = {
            self.SPEED_NORMAL: 0.75,        # 75% normal speed
            self.SPEED_FAST: 0.10,          # 10% fast
            self.SPEED_VERY_FAST: 0.05,     # 5% very fast
            self.SPEED_ULTRA_FAST: 0.02,    # 2% ultra fast
            self.SPEED_SLOW: 0.06,          # 6% slow
            self.SPEED_ULTRA_SLOW: 0.02     # 2% ultra slow
        }
    
    def select_speed(self, *args, **kwargs) -> Dict:
        """DISABLED - Returns 1.0x speed for all clips (pure cuts only)"""
        # Accept any parameters but always return 1.0x speed
        clip_data = kwargs.get('clip_data', args[1] if len(args) > 1 else {})
        return self._create_speed_params(self.SPEED_NORMAL, clip_data)
    
    def select_speed_OLD(self,
                    clip_index: int,
                    clip_data: Dict,
                    music_energy: float = 0.5,
                    beat_strength: float = 0.5,
                    is_drop: bool = False,
                    is_breakdown: bool = False) -> Dict:
        """
        Intelligently select clip speed based on context
        
        Args:
            clip_index: Current clip position
            clip_data: Clip data with analysis
            music_energy: Music energy 0-1 (1 = high energy)
            beat_strength: Beat strength 0-1 (1 = strong beat)
            is_drop: Is this a drop/climax moment?
            is_breakdown: Is this a breakdown/calm section?
        
        Returns:
            Dict with speed multiplier and FFmpeg parameters
        """
        
        # Extract clip energy
        clip_energy = clip_data.get('analysis', {}).get('energy', 5) / 10.0
        
        # Adjust weights based on context
        weights = self.base_weights.copy()
        
        # ? DROP/CLIMAX ? Fast speeds
        if is_drop or (music_energy > 0.85 and beat_strength > 0.8):
            weights[self.SPEED_ULTRA_FAST] = 0.40   # 40% ultra fast
            weights[self.SPEED_VERY_FAST] = 0.35    # 35% very fast
            weights[self.SPEED_FAST] = 0.20         # 20% fast
            weights[self.SPEED_NORMAL] = 0.05       # 5% normal
            weights[self.SPEED_SLOW] = 0.0
            weights[self.SPEED_ULTRA_SLOW] = 0.0
        
        # ?? BREAKDOWN ? Slow speeds
        elif is_breakdown or music_energy < 0.3:
            weights[self.SPEED_ULTRA_SLOW] = 0.25   # 25% ultra slow
            weights[self.SPEED_SLOW] = 0.40         # 40% slow
            weights[self.SPEED_NORMAL] = 0.30       # 30% normal
            weights[self.SPEED_FAST] = 0.05         # 5% fast
            weights[self.SPEED_VERY_FAST] = 0.0
            weights[self.SPEED_ULTRA_FAST] = 0.0
        
        # ?? HIGH ENERGY ? More fast speeds
        elif music_energy > 0.7:
            weights[self.SPEED_ULTRA_FAST] = 0.10
            weights[self.SPEED_VERY_FAST] = 0.20
            weights[self.SPEED_FAST] = 0.25
            weights[self.SPEED_NORMAL] = 0.40
            weights[self.SPEED_SLOW] = 0.05
            weights[self.SPEED_ULTRA_SLOW] = 0.0
        
        # ?? LOW ENERGY ? More normal/slow
        elif music_energy < 0.4:
            weights[self.SPEED_NORMAL] = 0.60
            weights[self.SPEED_SLOW] = 0.20
            weights[self.SPEED_FAST] = 0.15
            weights[self.SPEED_VERY_FAST] = 0.03
            weights[self.SPEED_ULTRA_FAST] = 0.01
            weights[self.SPEED_ULTRA_SLOW] = 0.01
        
        # Prevent slow-mo overuse (max 1 every 8 clips)
        if clip_index - self.last_slow_index < 8:
            weights[self.SPEED_ULTRA_SLOW] = 0
            weights[self.SPEED_SLOW] *= 0.5
        
        # Match clip energy to music energy
        energy_match = abs(clip_energy - music_energy)
        if energy_match > 0.4:
            # Mismatched energy ? use speed to compensate
            if clip_energy < music_energy:
                # Low energy clip, high energy music ? speed up
                weights[self.SPEED_FAST] *= 1.5
                weights[self.SPEED_VERY_FAST] *= 2.0
            else:
                # High energy clip, low energy music ? slow down
                weights[self.SPEED_SLOW] *= 1.5
                weights[self.SPEED_ULTRA_SLOW] *= 2.0
        
        # Normalize weights
        total = sum(weights.values())
        if total > 0:
            weights = {k: v/total for k, v in weights.items()}
        
        # Select speed
        speed = random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]
        
        # Track slow-mo usage
        if speed <= self.SPEED_SLOW:
            self.last_slow_index = clip_index
        
        # Track history
        self.speed_history.append(speed)
        
        # Return speed parameters
        return self._create_speed_params(speed, clip_data)
    
    def _create_speed_params(self, speed: float, clip_data: Dict) -> Dict:
        """Create FFmpeg speed change parameters"""
        
        if speed == self.SPEED_NORMAL:
            return {
                'speed': 1.0,
                'filter': None,
                'description': 'normal'
            }
        
        # Calculate PTS (presentation timestamp) multiplier
        # PTS multiplier is inverse of speed (2x speed = 0.5 PTS)
        pts = 1.0 / speed
        
        # Create filter string
        # setpts adjusts video timing, atempo adjusts audio (if present)
        filter_str = f'setpts={pts}*PTS'
        
        # Audio speed adjustment (if clip has audio)
        # Note: atempo only supports 0.5-2.0 range, need to chain for extreme speeds
        if speed >= 0.5 and speed <= 2.0:
            # Single atempo filter
            audio_filter = f'atempo={speed}'
        elif speed > 2.0:
            # Chain atempo filters (e.g. 4x = 2x * 2x)
            audio_filter = f'atempo=2.0,atempo={speed/2.0}'
        else:  # speed < 0.5
            # Chain atempo filters (e.g. 0.25x = 0.5x * 0.5x)
            audio_filter = f'atempo=0.5,atempo={speed/0.5}'
        
        # Speed description
        if speed >= 1.5:
            desc = f'{speed}x FAST'
        elif speed > 1.0:
            desc = f'{speed}x fast'
        elif speed < 0.75:
            desc = f'{speed}x SLOW-MO'
        else:
            desc = f'{speed}x slow'
        
        return {
            'speed': speed,
            'filter': filter_str,
            'audio_filter': audio_filter,
            'description': desc
        }
    
    def get_statistics(self) -> Dict:
        """Get speed variation usage statistics"""
        total = len(self.speed_history)
        if total == 0:
            return {}
        
        speeds = {
            '0.5x (ultra slow)': 0,
            '0.75x (slow)': 0,
            '1.0x (normal)': 0,
            '1.25x (fast)': 0,
            '1.5x (very fast)': 0,
            '2.0x (ultra fast)': 0
        }
        
        for s in self.speed_history:
            if s == 0.5:
                speeds['0.5x (ultra slow)'] += 1
            elif s == 0.75:
                speeds['0.75x (slow)'] += 1
            elif s == 1.0:
                speeds['1.0x (normal)'] += 1
            elif s == 1.25:
                speeds['1.25x (fast)'] += 1
            elif s == 1.5:
                speeds['1.5x (very fast)'] += 1
            elif s == 2.0:
                speeds['2.0x (ultra fast)'] += 1
        
        stats = {}
        for name, count in speeds.items():
            if count > 0:
                stats[name] = {
                    'count': count,
                    'percentage': (count / total) * 100
                }
        
        return stats


class MusicSectionDetector:
    """
    Detect musical sections (drops, breakdowns, build-ups)
    For speed variation intelligence
    """
    
    @staticmethod
    def is_drop(current_time: float, beat_times: list, energy: float) -> bool:
        """Detect if current moment is a drop/climax"""
        # Drop = high energy + strong beat
        return energy > 0.85
    
    @staticmethod
    def is_breakdown(current_time: float, energy: float, prev_energy: float) -> bool:
        """Detect if current moment is a breakdown"""
        # Breakdown = low energy after high energy
        energy_drop = prev_energy - energy
        return energy < 0.35 or energy_drop > 0.4
    
    @staticmethod
    def is_buildup(energy: float, prev_energy: float) -> bool:
        """Detect if current moment is building up"""
        # Build-up = steadily increasing energy
        energy_increase = energy - prev_energy
        return energy_increase > 0.2 and energy > 0.5




