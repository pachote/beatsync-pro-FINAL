import re

with open("video_renderer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add method to apply audio reactive effects
effects_method = '''
    def _apply_audio_reactive_effects(self, clip_dict: Dict, audio_reactive: Dict) -> Dict:
        """Apply audio-reactive effects (zoom, flash, speed) to clip"""
        if not audio_reactive:
            return clip_dict
        
        clip_start = clip_dict.get('start_time', 0)
        clip_end = clip_start + clip_dict.get('duration', 2.0)
        
        effects_filter = []
        
        # 1. ZOOM EVENTS - bass-reactive zoom pulses
        for zoom in audio_reactive.get('zoom_events', []):
            zoom_time = zoom['time']
            if clip_start <= zoom_time < clip_end:
                # Zoom pulse: 1.0 -> (1.0 + strength) -> 1.0
                strength = zoom.get('strength', 0.2)
                duration = zoom.get('duration', 0.1)
                
                # Calculate relative time in clip
                rel_time = zoom_time - clip_start
                
                # Zoom in and out over duration
                zoom_filter = f"zoompan=z='if(between(t,{rel_time},{rel_time+duration}),1+{strength}*(sin((t-{rel_time})*PI/{duration})),1)':d=1:s=1920x1080"
                effects_filter.append(zoom_filter)
                
                print(f"       🔍 Zoom pulse @ {zoom_time:.2f}s (strength: {strength})")
        
        # 2. FLASH EVENTS - snare-reactive brightness
        for flash in audio_reactive.get('flash_events', []):
            flash_time = flash['time']
            if clip_start <= flash_time < clip_end:
                intensity = flash.get('intensity', 0.3)
                duration = flash.get('duration', 0.05)
                
                rel_time = flash_time - clip_start
                
                # Quick brightness flash
                flash_filter = f"eq=brightness='if(between(t,{rel_time},{rel_time+duration}),{intensity}*(1-abs((t-{rel_time}-{duration/2})*2/{duration})),0)'"
                effects_filter.append(flash_filter)
        
        # 3. SPEED VARIATIONS - buildups and drops
        for speed_var in audio_reactive.get('speed_variations', []):
            var_start = speed_var['start']
            var_end = speed_var['end']
            
            # Check if this clip overlaps with speed variation
            if not (clip_end < var_start or clip_start > var_end):
                start_speed = speed_var.get('start_speed', 1.0)
                end_speed = speed_var.get('end_speed', 1.0)
                var_type = speed_var.get('type', '')
                
                # Calculate speed at this clip's position
                if var_start <= clip_start <= var_end:
                    progress = (clip_start - var_start) / (var_end - var_start)
                    clip_speed = start_speed + (end_speed - start_speed) * progress
                    clip_dict['speed'] = round(clip_speed, 2)
                    print(f"       ⚡ Speed: {clip_speed:.2f}x ({var_type})")
        
        # Combine effects into ffmpeg filter
        if effects_filter:
            existing_filter = clip_dict.get('effects', {}).get('ffmpeg_filter', '')
            combined = ','.join([f for f in [existing_filter] + effects_filter if f])
            clip_dict['effects']['ffmpeg_filter'] = combined
        
        return clip_dict
'''

# Add the method before render_video
if "_apply_audio_reactive_effects" not in content:
    content = content.replace(
        "def render_video(",
        effects_method + "\n    def render_video("
    )

# Apply effects to each clip during rendering
if "self._apply_audio_reactive_effects" not in content:
    # Find where clips are processed
    old_process = "enhanced = self.apply_all_engines(clip, i, music_duration, beat_times, previous)"
    new_process = '''enhanced = self.apply_all_engines(clip, i, music_duration, beat_times, previous)
            
            # APPLY AUDIO REACTIVE EFFECTS (superhuman sync)
            audio_reactive = audio_data.get('audio_reactive', {})
            if audio_reactive:
                enhanced = self._apply_audio_reactive_effects(enhanced, audio_reactive)'''
    
    content = content.replace(old_process, new_process)

with open("video_renderer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Video renderer now APPLIES audio reactive effects!")
