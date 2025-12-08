"""
BeatSync PRO - Transitions Engine
"""

class TransitionEffects:
    """Handle transitions between clips"""
    
    def __init__(self):
        self.enabled = True
    
    def get_transition(self, transition_type: str, duration: float = 0.3) -> dict:
        """
        Get transition settings for FFmpeg
        Returns dict with transition info
        """
        if transition_type == 'flash':
            return self.get_flash_transition(duration)
        elif transition_type == 'dissolve':
            return self.get_dissolve_transition(duration)
        elif transition_type == 'glitch':
            return self.get_glitch_transition(duration)
        elif transition_type == 'zoom':
            return self.get_zoom_transition(duration)
        elif transition_type == 'slide':
            return self.get_slide_transition(duration)
        else:
            return {'type': 'cut', 'duration': 0}  # Hard cut
    
    def get_flash_transition(self, duration: float = 0.3) -> dict:
        """White flash between clips"""
        return {
            'type': 'flash',
            'duration': duration,
            'filter': 'fade=t=out:st=0:d=0.15:color=white,fade=t=in:st=0.15:d=0.15:color=white'
        }
    
    def get_dissolve_transition(self, duration: float = 0.5) -> dict:
        """Crossfade dissolve"""
        return {
            'type': 'dissolve',
            'duration': duration,
            'filter': f'xfade=transition=fade:duration={duration}:offset=0'
        }
    
    def get_glitch_transition(self, duration: float = 0.2) -> dict:
        """Glitchy cut with noise burst"""
        return {
            'type': 'glitch',
            'duration': duration,
            'filter': 'noise=alls=100:allf=t+u'
        }
    
    def get_zoom_transition(self, duration: float = 0.4) -> dict:
        """Zoom out from previous, zoom into next"""
        return {
            'type': 'zoom',
            'duration': duration,
            'filter': 'scale=iw*0.5:ih*0.5,scale=1920:1080'
        }
    
    def get_slide_transition(self, duration: float = 0.3) -> dict:
        """Slide transition"""
        return {
            'type': 'slide',
            'duration': duration,
            'filter': 'xfade=transition=slideleft:duration=0.3:offset=0'
        }
