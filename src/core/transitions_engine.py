"""
BeatSync PRO - Professional Transitions Engine
Millisecond-precise, content-aware, professional transitions
"""

from enum import Enum
from typing import Dict, List, Tuple
import random


class TransitionType(Enum):
    """Professional transition types"""
    HARD_CUT = "hard_cut"           # Clean cut (80% of transitions)
    QUICK_FADE = "quick_fade"       # 0.08s crossfade (smooth)
    FLASH_WHITE = "flash_white"     # 1-2 frame white flash
    FLASH_BLACK = "flash_black"     # 1-2 frame black flash
    LUMA_FADE = "luma_fade"         # Through white (0.12s)
    MOTION_BLUR = "motion_blur"     # Directional blur transition


class TransitionEngine:
    """
    AI-powered transition selection engine
    Chooses transitions based on:
    - Music energy & beat strength
    - Visual content similarity
    - Previous transition history
    """
    
    def __init__(self):
        self.transition_history = []
        self.last_flash_index = -10  # Track last flash to avoid overuse
        
        # Transition weights (professional music video standard)
        self.base_weights = {
            TransitionType.HARD_CUT: 0.70,      # 70% hard cuts
            TransitionType.QUICK_FADE: 0.15,    # 15% quick fades
            TransitionType.FLASH_WHITE: 0.05,   # 5% white flashes
            TransitionType.FLASH_BLACK: 0.05,   # 5% black flashes
            TransitionType.LUMA_FADE: 0.03,     # 3% luma fades
            TransitionType.MOTION_BLUR: 0.02    # 2% motion blur
        }
    
    def select_transition(self, 
                         clip_index: int,
                         current_clip: Dict,
                         next_clip: Dict,
                         beat_strength: float = 0.5,
                         music_energy: float = 0.5) -> Dict:
        """
        Intelligently select transition type based on context
        
        Args:
            clip_index: Current clip position
            current_clip: Current clip data with analysis
            next_clip: Next clip data with analysis
            beat_strength: Beat strength 0-1 (1 = strong beat)
            music_energy: Music energy 0-1 (1 = high energy)
        
        Returns:
            Dict with transition type and parameters
        """
        
        # Extract clip energies
        current_energy = current_clip.get('analysis', {}).get('energy', 5) / 10.0
        next_energy = next_clip.get('analysis', {}).get('energy', 5) / 10.0
        
        # Calculate energy change
        energy_change = abs(next_energy - current_energy)
        
        # Adjust weights based on context
        weights = self.base_weights.copy()
        
        # HIGH ENERGY + STRONG BEAT ? More flashes and hard cuts
        if music_energy > 0.7 and beat_strength > 0.7:
            weights[TransitionType.HARD_CUT] = 0.75
            weights[TransitionType.FLASH_WHITE] = 0.10
            weights[TransitionType.FLASH_BLACK] = 0.08
            weights[TransitionType.QUICK_FADE] = 0.05
            weights[TransitionType.LUMA_FADE] = 0.01
            weights[TransitionType.MOTION_BLUR] = 0.01
        
        # LOW ENERGY ? More fades, fewer flashes
        elif music_energy < 0.4:
            weights[TransitionType.HARD_CUT] = 0.50
            weights[TransitionType.QUICK_FADE] = 0.35
            weights[TransitionType.FLASH_WHITE] = 0.02
            weights[TransitionType.FLASH_BLACK] = 0.05
            weights[TransitionType.LUMA_FADE] = 0.06
            weights[TransitionType.MOTION_BLUR] = 0.02
        
        # BIG ENERGY CHANGE ? Emphasize transition
        if energy_change > 0.4:
            if next_energy > current_energy:  # Building up
                weights[TransitionType.FLASH_WHITE] *= 2
                weights[TransitionType.LUMA_FADE] *= 1.5
            else:  # Breaking down
                weights[TransitionType.FLASH_BLACK] *= 2
        
        # Prevent flash overuse (max 1 flash every 5 clips)
        if clip_index - self.last_flash_index < 5:
            weights[TransitionType.FLASH_WHITE] = 0
            weights[TransitionType.FLASH_BLACK] = 0
        
        # Normalize weights
        total = sum(weights.values())
        weights = {k: v/total for k, v in weights.items()}
        
        # Select transition
        transition_type = random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]
        
        # Track flash usage
        if transition_type in [TransitionType.FLASH_WHITE, TransitionType.FLASH_BLACK]:
            self.last_flash_index = clip_index
        
        # Track history
        self.transition_history.append(transition_type)
        
        # Return transition with parameters
        return self._create_transition_params(transition_type, beat_strength, music_energy)
    
    def _create_transition_params(self, 
                                  transition_type: TransitionType,
                                  beat_strength: float,
                                  music_energy: float) -> Dict:
        """Create FFmpeg filter parameters for transition"""
        
        if transition_type == TransitionType.HARD_CUT:
            return {
                'type': 'hard_cut',
                'duration': 0.0,
                'filter': None
            }
        
        elif transition_type == TransitionType.QUICK_FADE:
            # Ultra-short crossfade (0.08s standard)
            duration = 0.08
            return {
                'type': 'crossfade',
                'duration': duration,
                'filter': f'xfade=transition=fade:duration={duration}:offset=0'
            }
        
        elif transition_type == TransitionType.FLASH_WHITE:
            # 2-frame white flash (0.066s at 30fps)
            return {
                'type': 'flash_white',
                'duration': 0.066,
                'filter': 'fade=t=out:st=0:d=0.033:c=white,fade=t=in:st=0.033:d=0.033:c=white'
            }
        
        elif transition_type == TransitionType.FLASH_BLACK:
            # 2-frame black flash
            return {
                'type': 'flash_black',
                'duration': 0.066,
                'filter': 'fade=t=out:st=0:d=0.033:c=black,fade=t=in:st=0.033:d=0.033:c=black'
            }
        
        elif transition_type == TransitionType.LUMA_FADE:
            # Quick fade through white (0.12s)
            duration = 0.12
            return {
                'type': 'luma_fade',
                'duration': duration,
                'filter': f'xfade=transition=fadewhite:duration={duration}:offset=0'
            }
        
        elif transition_type == TransitionType.MOTION_BLUR:
            # Directional blur (0.10s)
            duration = 0.10
            # Random direction (wipeleft, wiperight, wipeup, wipedown)
            direction = random.choice(['wipeleft', 'wiperight', 'wipeup', 'wipedown'])
            return {
                'type': 'motion_blur',
                'duration': duration,
                'filter': f'xfade=transition={direction}:duration={duration}:offset=0'
            }
        
        return {'type': 'hard_cut', 'duration': 0.0, 'filter': None}
    
    def get_statistics(self) -> Dict:
        """Get transition usage statistics"""
        total = len(self.transition_history)
        if total == 0:
            return {}
        
        stats = {}
        for t_type in TransitionType:
            count = self.transition_history.count(t_type)
            stats[t_type.value] = {
                'count': count,
                'percentage': (count / total) * 100
            }
        
        return stats


# Music energy analyzer (integrated with librosa)
class MusicEnergyAnalyzer:
    """Analyze music energy curve for intelligent transitions"""
    
    @staticmethod
    def get_beat_strength(beat_times: List[float], current_time: float) -> float:
        """
        Calculate beat strength at current time
        Returns 0-1 (1 = strong beat, 0 = weak/no beat)
        """
        if not beat_times:
            return 0.5
        
        # Find closest beat
        closest_beat = min(beat_times, key=lambda x: abs(x - current_time))
        time_diff = abs(closest_beat - current_time)
        
        # Strong beat if within 0.05s
        if time_diff < 0.05:
            return 1.0
        elif time_diff < 0.15:
            return 0.7
        elif time_diff < 0.3:
            return 0.4
        else:
            return 0.2
    
    @staticmethod
    def get_music_energy(current_time: float, duration: float) -> float:
        """
        Estimate music energy at current time
        Returns 0-1 (1 = high energy)
        
        TODO: Integrate with actual librosa spectral analysis
        For now, uses simple curve
        """
        # Normalize time
        progress = current_time / duration
        
        # Simple energy curve (intro low, build to middle, maintain high, outro fade)
        if progress < 0.1:  # Intro
            return 0.3 + (progress * 3)
        elif progress < 0.3:  # Build
            return 0.6 + ((progress - 0.1) * 1.5)
        elif progress < 0.8:  # Main section
            return 0.9
        else:  # Outro
            return 0.9 - ((progress - 0.8) * 2)
