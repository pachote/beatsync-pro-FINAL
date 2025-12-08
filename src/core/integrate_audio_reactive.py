import re

with open("video_renderer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add audio analyzer import if not present
if "from .audio_analyzer import AudioAnalyzer" not in content:
    content = content.replace(
        "from .speed_variations import SpeedVariationEngine",
        "from .speed_variations import SpeedVariationEngine\nfrom .audio_analyzer import AudioAnalyzer"
    )

# Initialize audio analyzer in __init__
if "self.audio_analyzer" not in content:
    content = content.replace(
        "self.speed_engine = SpeedVariationEngine()",
        "self.speed_engine = SpeedVariationEngine()\n        self.audio_analyzer = AudioAnalyzer()"
    )

# Add audio analysis to render_music_video method
old_render_music = """def render_music_video(self, edit_plan, music_path, output_path):
        \"\"\"Main entry point - matches GUI expectations\"\"\"
        clips = edit_plan.get('clips', [])
        aesthetic_style = edit_plan.get('aesthetic_style', 'Modern')
        return self.render_video(clips, music_path, output_path, aesthetic_style)"""

new_render_music = """def render_music_video(self, edit_plan, music_path, output_path):
        \"\"\"Main entry point - matches GUI expectations\"\"\"
        clips = edit_plan.get('clips', [])
        aesthetic_style = edit_plan.get('aesthetic_style', 'Modern')
        
        # Analyze audio for reactive effects
        print("\\n  🎵 Analyzing audio for reactive effects...")
        self.audio_data = self.audio_analyzer.analyze_audio(music_path)
        print(f"  ✅ Audio analysis complete!")
        
        return self.render_video(clips, music_path, output_path, aesthetic_style)"""

content = content.replace(old_render_music, new_render_music)

# Now add the reactive effects application in the rendering loop
# Find the apply_all_engines line and add audio reactive after it
old_apply = """enhanced = self.apply_all_engines(clip, i, music_duration, beat_times, previous)
            enhanced_clips.append(enhanced)"""

new_apply = """enhanced = self.apply_all_engines(clip, i, music_duration, beat_times, previous)
            
            # Apply audio reactive effects if available
            if hasattr(self, 'audio_data') and self.audio_data:
                audio_reactive = self.audio_data.get('audio_reactive', {})
                if audio_reactive:
                    enhanced = self._apply_audio_reactive_effects(enhanced, audio_reactive)
            
            enhanced_clips.append(enhanced)"""

content = content.replace(old_apply, new_apply)

with open("video_renderer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Audio reactive effects properly integrated!")
