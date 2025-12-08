import re

with open("audio_analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add import
if "audio_reactive_engine" not in content:
    content = content.replace(
        "from .music_structure_analyzer import music_structure_analyzer",
        "from .music_structure_analyzer import music_structure_analyzer\nfrom .audio_reactive_engine import audio_reactive_engine"
    )

# Add audio reactive analysis after music structure
if "audio_reactive" not in content:
    insert_point = 'audio_data["music_structure"] = music_structure'
    addition = '''audio_data["music_structure"] = music_structure
            
            # Audio Reactive Effects for superhuman sync
            print("  🎛️ Analyzing audio reactivity...")
            audio_reactive = audio_reactive_engine.analyze_for_effects(audio_path, music_structure)
            audio_data["audio_reactive"] = audio_reactive'''
    
    content = content.replace(insert_point, addition)

with open("audio_analyzer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Audio analyzer now includes reactive effects!")
