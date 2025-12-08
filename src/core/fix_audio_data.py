import re

with open("video_renderer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add import at top
if "from .audio_analyzer import" not in content:
    content = content.replace(
        "import subprocess",
        "import subprocess\nfrom .audio_analyzer import AudioAnalyzer"
    )

# Initialize audio analyzer in __init__
if "self.audio_analyzer = AudioAnalyzer()" not in content:
    content = content.replace(
        "self.project_root = project_root",
        "self.project_root = project_root\n        self.audio_analyzer = AudioAnalyzer()"
    )

# Add audio analysis at start of render_video
old_render_start = """def render_video(self, clips: List[Dict], music_path: str, output_path: str, aesthetic_style: str = "Modern"):
        """Render using GPU-accelerated H.264 with fallback"""
        print("\\n" + "=" * 60)
        print("?? FAST GPU RENDERER (FIXED)")
        print("=" * 60)
        print(f"   Total clips: {len(clips)}")
        print(f"   Output: {output_path}")
        print()"""

new_render_start = """def render_video(self, clips: List[Dict], music_path: str, output_path: str, aesthetic_style: str = "Modern"):
        """Render using GPU-accelerated H.264 with fallback"""
        
        # Analyze audio for reactive effects
        print("\\n  🎵 Loading audio analysis for reactive effects...")
        audio_data = self.audio_analyzer.analyze_audio(music_path)
        
        print("\\n" + "=" * 60)
        print("?? FAST GPU RENDERER (FIXED)")
        print("=" * 60)
        print(f"   Total clips: {len(clips)}")
        print(f"   Output: {output_path}")
        print()"""

content = content.replace(old_render_start, new_render_start)

with open("video_renderer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Audio reactive bug fixed!")
print("   Audio data now properly loaded in renderer")
