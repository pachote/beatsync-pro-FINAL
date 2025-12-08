"""
BeatSync PRO - Beat Effects WITH WORKING TEMPORAL SYNC
"""

class BeatReactiveEffects:

    def __init__(self):
        self.enabled = True

    def get_energy_based_effect(self, energy_level: int, effect_type: str = 'beat_flash', 
                                clip_start: float = None, clip_end: float = None, 
                                beat_times: list = None) -> str:
        """Route to specific effect - NOW WITH TIMING"""
        intensity = min(max(energy_level / 10.0, 0.6), 1.0)

        # Effects that need beat timing
        if effect_type == 'beat_flash':
            if clip_start is not None and clip_end is not None and beat_times is not None:
                return self.get_beat_flash(clip_start, clip_end, beat_times, intensity)
            else:
                return ""  # No timing info, skip effect
        
        # Effects that DON'T need timing (constant effects)
        elif effect_type == 'camera_shake':
            if clip_start is not None and clip_end is not None and beat_times is not None:
                return self.get_camera_shake(clip_start, clip_end, beat_times, intensity)
            else:
                return ""
        elif effect_type == 'glitch':
            return self.get_glitch_effect(intensity)
        elif effect_type == 'zoom_pulse':
            if clip_start is not None and clip_end is not None and beat_times is not None:
                return self.get_zoom_pulse(clip_start, clip_end, beat_times, intensity)
            else:
                return ""
        elif effect_type == 'saturation_pulse':
            if clip_start is not None and clip_end is not None and beat_times is not None:
                return self.get_saturation_pulse(clip_start, clip_end, beat_times, intensity)
        elif effect_type == 'color_shift':
            if clip_start is not None and clip_end is not None and beat_times is not None:
                return self.get_color_shift(clip_start, clip_end, beat_times, intensity)
            else:
                return ""
        else:
            return ""

    def get_beat_flash(self, clip_start: float, clip_end: float, 
                       beat_times: list, intensity: float = 0.7) -> str:
        """TIME-SYNCHRONIZED brightness flash"""
        # Filter beats to this clip's time range
        clip_beats = [b for b in beat_times if clip_start <= b < clip_end]
        
        if not clip_beats:
            print(f"      ⚠️ No beats in range {clip_start:.2f}-{clip_end:.2f}s")
            return ""
        
        flash_duration = 0.03  # 30ms - almost subliminal
        flash_amount = 0.03 + (intensity * 0.05)  # Range: 0.03-0.08 (3-8% boost) - subtle but visible
        
        # Build temporal conditions
        conditions = []
        for beat in clip_beats:
            relative_time = beat - clip_start
            beat_end = relative_time + flash_duration
            conditions.append(f"between(t\\,{relative_time:.3f}\\,{beat_end:.3f})")
        
        combined = '+'.join(conditions)
        filter_str = f"eq=brightness='if({combined}\\,{flash_amount}\\,0)':eval=frame"
        
        print(f"      ✅ Beat flash: {len(clip_beats)} flashes")
        return filter_str

    def get_camera_shake(self, clip_start: float, clip_end: float,
                         beat_times: list, intensity: float = 0.7) -> str:
        """BEAT-REACTIVE camera shake - SELECTIVE for impact"""
        clip_beats = [b for b in beat_times if clip_start <= b < clip_end]
        
        if not clip_beats:
            return ""
        
        # DYNAMIC: Only shake on every 3rd beat for rhythm
        selected_beats = [clip_beats[i] for i in range(0, len(clip_beats), 3)]
        
        if not selected_beats:
            return ""
        
        # DYNAMIC amplitude based on intensity
        amplitude = int(4 + (intensity * 8))  # Range: 4-12 pixels (more variation)
        shake_duration = 0.15  # 150ms
        frequency = 30  # Fast for impact
        
        # Build temporal conditions
        conditions = []
        for beat in selected_beats:
            relative_time = beat - clip_start
            conditions.append(f"between(t\\,{relative_time:.3f}\\,{relative_time + shake_duration:.3f})")
        
        combined = '+'.join(conditions)
        amp_expr = f"if({combined}\\,{amplitude}\\,0)"
        
        filter_str = f"crop=in_w-{amplitude*2}:in_h-{amplitude*2}:x='{amplitude}+{amp_expr}*sin(2*PI*t*{frequency})':y='{amplitude}+{amp_expr}*cos(2*PI*t*{frequency})'"
        
        print(f"      ✅ Beat shake: {len(selected_beats)} shakes (every 3rd beat)")
        return filter_str
    def get_glitch_effect(self, intensity: float = 0.7) -> str:
        """Glitch - DISABLED (noise filter crashes FFmpeg on Windows)"""
        return ""  # Disabled - use other effects instead
    def get_zoom_pulse(self, clip_start: float, clip_end: float,
                       beat_times: list, intensity: float = 0.7) -> str:
        """Zoom pulse - DISABLED (zoompan incompatible with temporal expressions)"""
        return ""  # Disabled - use beat_flash or saturation_pulse instead
    def get_saturation_pulse(self, clip_start: float, clip_end: float,
                            beat_times: list, intensity: float = 0.7) -> str:
        """TIME-SYNCHRONIZED saturation"""
        clip_beats = [b for b in beat_times if clip_start <= b < clip_end]
        
        if not clip_beats:
            return ""
        
        sat_amount = 1.0 + (intensity * 1.0)
        pulse_duration = 0.1
        
        conditions = []
        for beat in clip_beats:
            relative_time = beat - clip_start
            conditions.append(f"between(t\\,{relative_time:.3f}\\,{relative_time + pulse_duration:.3f})")
        
        combined = '+'.join(conditions)
        filter_str = f"eq=saturation='if({combined}\\,{sat_amount}\\,1.0)':eval=frame"
        
        print(f"      ✅ Saturation pulse: {len(clip_beats)} pulses")
        return filter_str

    def get_chromatic_aberration(self, intensity: float = 0.7) -> str:
        return ""

    def get_color_shift(self, clip_start: float, clip_end: float,
                        beat_times: list, intensity: float = 0.7) -> str:
        """Color shift - DISABLED (hue filter crashes FFmpeg on Windows)"""
        return ""  # Disabled - use beat_flash + saturation_pulse instead
    def get_bass_drop_effect(self, intensity: float = 1.0) -> str:
        return ""
