"""
BeatSync PRO - Color Grading Engine
Professional color presets for stunning visuals
"""

class ColorGradingEngine:
    """Apply professional color grading to videos"""
    
    def __init__(self):
        self.presets = {
            'cinematic': self._cinematic_preset,
            'cyberpunk': self._cyberpunk_preset,
            'vintage': self._vintage_preset,
            'high_contrast': self._high_contrast_preset,
            'neon_dream': self._neon_dream_preset,
            'warm_sunset': self._warm_sunset_preset,
            'cool_blue': self._cool_blue_preset,
            'none': self._no_grading
        }
    
    def get_ffmpeg_filter(self, preset_name: str, intensity: float = 1.0) -> str:
        """Get FFmpeg filter string for color grading"""
        if preset_name not in self.presets:
            preset_name = 'none'
        return self.presets[preset_name](intensity)
    
    def _cinematic_preset(self, intensity: float) -> str:
        """Hollywood teal/orange look"""
        i = intensity
        return (
            f"curves="
            f"r='0/0 0.5/{0.45 + (0.1 * i)} 1/1':"
            f"g='0/0 0.5/{0.48 + (0.05 * i)} 1/1':"
            f"b='0/{0.1 * i} 0.5/0.5 1/{0.9 + (0.1 * i)}',"
            f"eq=contrast={1.1 + (0.2 * i)}:saturation={1.1 + (0.3 * i)}"
        )
    
    def _cyberpunk_preset(self, intensity: float) -> str:
        """Neon pink/blue futuristic look"""
        i = intensity
        return (
            f"eq=contrast={1.2 + (0.3 * i)}:saturation={1.5 + (0.5 * i)}:gamma={0.9},"
            f"curves="
            f"r='0/{0.1 * i} 0.5/{0.6 + (0.1 * i)} 1/1':"
            f"g='0/0 0.5/{0.45} 1/{0.95}':"
            f"b='0/{0.15 * i} 0.5/{0.55 + (0.1 * i)} 1/1',"
            f"hue=h={-10 * i}:s={1 + (0.3 * i)}"
        )
    
    def _vintage_preset(self, intensity: float) -> str:
        """Warm, faded film look"""
        i = intensity
        return (
            f"curves="
            f"r='0/{0.05 * i} 1/{0.95 - (0.05 * i)}':"
            f"g='0/{0.05 * i} 1/{0.95 - (0.05 * i)}':"
            f"b='0/{0.1 * i} 1/{0.9 - (0.1 * i)}',"
            f"eq=contrast={0.9 - (0.1 * i)}:saturation={0.8 - (0.2 * i)}:gamma={1.1 + (0.1 * i)},"
            f"colortemperature={3000 + (1000 * i)}"
        )
    
    def _high_contrast_preset(self, intensity: float) -> str:
        """Dramatic blacks and whites"""
        i = intensity
        return (
            f"eq=contrast={1.3 + (0.5 * i)}:brightness={-0.05 * i}:saturation={0.9 - (0.3 * i)},"
            f"curves=all='0/0 0.3/{0.2 - (0.05 * i)} 0.7/{0.8 + (0.05 * i)} 1/1'"
        )
    
    def _neon_dream_preset(self, intensity: float) -> str:
        """Vibrant, saturated colors"""
        i = intensity
        return (
            f"eq=contrast={1.2 + (0.2 * i)}:saturation={1.6 + (0.8 * i)}:gamma={0.95},"
            f"vibrance={0.3 * i},"
            f"curves=all='0/{0.05 * i} 1/{0.95 + (0.05 * i)}'"
        )
    
    def _warm_sunset_preset(self, intensity: float) -> str:
        """Golden hour warmth"""
        i = intensity
        return (
            f"curves="
            f"r='0/0 0.5/{0.55 + (0.1 * i)} 1/1':"
            f"g='0/0 0.5/{0.52 + (0.08 * i)} 1/1':"
            f"b='0/0 0.5/{0.45 - (0.05 * i)} 1/{0.95}',"
            f"eq=contrast={1.05 + (0.1 * i)}:saturation={1.2 + (0.3 * i)},"
            f"colortemperature={2500 + (500 * i)}"
        )
    
    def _cool_blue_preset(self, intensity: float) -> str:
        """Cold, moonlight aesthetic"""
        i = intensity
        return (
            f"curves="
            f"r='0/0 0.5/{0.45 - (0.05 * i)} 1/{0.95}':"
            f"g='0/0 0.5/{0.48} 1/{0.98}':"
            f"b='0/{0.05 * i} 0.5/{0.55 + (0.1 * i)} 1/1',"
            f"eq=contrast={1.1 + (0.2 * i)}:saturation={0.9 + (0.2 * i)},"
            f"colortemperature={9000 + (2000 * i)}"
        )
    
    def _no_grading(self, intensity: float) -> str:
        """No color grading applied"""
        return ""
    
    def get_preset_names(self) -> list:
        """Get list of available preset names"""
        return list(self.presets.keys())
