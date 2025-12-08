"""
BeatSync PRO - Camera Motion Engine
Ken Burns effects, parallax, dynamic camera movement
"""

class CameraMotion:
    """Apply camera motion effects to clips"""
    
    def __init__(self):
        self.motion_types = {
            'ken_burns': self._ken_burns_effect,
            'zoom_in': self._zoom_in,
            'zoom_out': self._zoom_out,
            'pan_left': self._pan_left,
            'pan_right': self._pan_right,
            'shake': self._camera_shake,
            'static': self._no_motion
        }
    
    def get_motion_filter(self, motion_type: str, duration: float, intensity: float = 1.0) -> str:
        """
        Get FFmpeg filter for camera motion
        
        Args:
            motion_type: Type of motion
            duration: Clip duration
            intensity: Motion intensity
        """
        if motion_type not in self.motion_types:
            motion_type = 'static'
        
        return self.motion_types[motion_type](duration, intensity)
    
    def _ken_burns_effect(self, duration: float, intensity: float) -> str:
        """Classic Ken Burns slow zoom + pan"""
        zoom_speed = 0.001 * intensity
        pan_speed = 50 * intensity
        
        return (
            f"zoompan=z='min(zoom+{zoom_speed},1.5)':"
            f"x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)+(t*{pan_speed})':"
            f"d={int(duration*30)}:s=1920x1080:fps=30"
        )
    
    def _zoom_in(self, duration: float, intensity: float) -> str:
        """Zoom into the frame"""
        zoom_amount = 1.0 + (0.3 * intensity)
        
        return (
            f"zoompan=z='min(zoom+0.002*{intensity},{zoom_amount})':"
            f"d={int(duration*30)}:s=1920x1080:fps=30"
        )
    
    def _zoom_out(self, duration: float, intensity: float) -> str:
        """Zoom out from frame"""
        zoom_start = 1.0 + (0.3 * intensity)
        
        return (
            f"zoompan=z='max(zoom-0.002*{intensity},1.0)':"
            f"d={int(duration*30)}:s=1920x1080:fps=30"
        )
    
    def _pan_left(self, duration: float, intensity: float) -> str:
        """Pan camera left"""
        pan_speed = 100 * intensity
        
        return (
            f"crop=w=in_w:h=in_h:"
            f"x='max(0,t*{pan_speed})':"
            f"y=0"
        )
    
    def _pan_right(self, duration: float, intensity: float) -> str:
        """Pan camera right"""
        pan_speed = 100 * intensity
        
        return (
            f"crop=w=in_w:h=in_h:"
            f"x='max(0,in_w-w-t*{pan_speed})':"
            f"y=0"
        )
    
    def _camera_shake(self, duration: float, intensity: float) -> str:
        """Energetic camera shake"""
        shake_amount = int(10 * intensity)
        
        return (
            f"crop=in_w-{shake_amount*2}:in_h-{shake_amount*2}:"
            f"x='{shake_amount}+{shake_amount}*sin(2*PI*t*10)':"
            f"y='{shake_amount}+{shake_amount}*cos(2*PI*t*10)'"
        )
    
    def _no_motion(self, duration: float, intensity: float) -> str:
        """No camera motion"""
        return ""
    
    def select_smart_motion(self, energy: int, mood: str, duration: float) -> str:
        """
        Intelligently select camera motion based on energy and mood
        
        Args:
            energy: Energy level 1-10
            mood: Clip mood
            duration: Clip duration
        """
        # High energy = dynamic motion
        if energy >= 8:
            if duration < 1.5:
                return 'shake'  # Short clips = shake
            else:
                return 'zoom_in'  # Long clips = zoom
        
        # Medium energy = smooth motion
        elif energy >= 5:
            if 'mystical' in mood:
                return 'ken_burns'
            else:
                return 'zoom_in'
        
        # Low energy = minimal motion
        else:
            if duration > 3.0:
                return 'ken_burns'  # Slow elegance
            else:
                return 'static'
