"""
BeatSync PRO - Intelligent Speed Engine
AI-powered speed variations synchronized to music energy
"""

class SpeedEngine:
    """Handle intelligent speed variations"""
    
    def __init__(self):
        self.enabled = True
    
    def get_speed_for_clip(self, energy_level: int, mood: str, clip_index: int) -> float:
        """
        Intelligently determine speed based on:
        - Music energy (1-10)
        - Emotional mood
        - Clip variety (avoid repetition)
        
        Returns: speed multiplier (0.5 = half speed, 2.0 = double speed)
        """
        
        # Energy-based speed decisions
        if energy_level >= 9:
            # HIGH ENERGY - fast cuts or slow-mo for impact
            return 1.5 if clip_index % 3 == 0 else 1.0
        
        elif energy_level >= 7:
            # MEDIUM-HIGH - mostly normal with occasional speed
            return 1.2 if clip_index % 4 == 0 else 1.0
        
        elif energy_level >= 5:
            # MEDIUM - normal speed
            return 1.0
        
        elif energy_level >= 3:
            # LOW-MEDIUM - occasional slow-mo for drama
            return 0.8 if clip_index % 5 == 0 else 1.0
        
        else:
            # LOW ENERGY - slow, dramatic
            return 0.75
    
    def get_speed_filter(self, speed_multiplier: float) -> str:
        """
        Convert speed multiplier to FFmpeg filter
        """
        if speed_multiplier == 1.0:
            return ""  # No speed change
        
        # FFmpeg setpts filter (lower = faster, higher = slower)
        pts_value = 1.0 / speed_multiplier
        
        return f"setpts={pts_value}*PTS"
    
    def get_beat_sync_speed(self, beat_strength: float, base_speed: float = 1.0) -> float:
        """
        Micro-speed adjustments synchronized to individual beats
        Creates that "impossible coordination" feeling
        """
        # Slight speed variations on strong beats (0.95-1.05x)
        speed_variance = 0.05 * beat_strength
        return base_speed + speed_variance
