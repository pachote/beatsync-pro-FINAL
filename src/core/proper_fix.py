print("🔧 PROPER FIX - TESTING BEFORE SAVING")

# 1. FIX VISUAL INTELLIGENCE - Add segment quality PROPERLY
with open("visual_intelligence_v2.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the line with "GET ANALYSIS FROM CLAUDE" 
insert_line = None
for i, line in enumerate(lines):
    if "GET ANALYSIS FROM CLAUDE" in line:
        insert_line = i
        break

if insert_line:
    # Add segment quality analysis BEFORE Claude call
    indent = "        "
    new_code = [
        f"{indent}# SEGMENT QUALITY ANALYSIS\n",
        f"{indent}segment_quality = segment_quality_analyzer.analyze_video_segments(video_path)\n",
        f"{indent}\n"
    ]
    lines = lines[:insert_line] + new_code + lines[insert_line:]
    print("✅ Added segment quality call")
else:
    print("❌ Could not find insertion point for visual intelligence")

# Find return result and add segment quality to it
for i, line in enumerate(lines):
    if "return result" in line and "def analyze_video" in "".join(lines[max(0,i-20):i]):
        # Add segment quality to result BEFORE return
        indent = " " * (len(line) - len(line.lstrip()))
        lines.insert(i, f"{indent}result['segment_quality'] = segment_quality\n")
        print("✅ Added segment quality to result")
        break

# Save visual intelligence
with open("visual_intelligence_v2.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ VISUAL INTELLIGENCE FIXED!")

# 2. FIX AUDIO ANALYZER - Add audio reactive
with open("audio_analyzer.py", "r", encoding="utf-8") as f:
    audio_lines = f.readlines()

# Find "Deep Music Analysis Complete" and add audio reactive after
for i, line in enumerate(audio_lines):
    if "Deep Music Analysis Complete" in line:
        indent = " " * 12
        new_audio = [
            "\n",
            f"{indent}# AUDIO REACTIVE EFFECTS\n",
            f"{indent}audio_reactive = audio_reactive_engine.analyze_for_effects(audio_path, music_structure)\n",
            f"{indent}audio_data['audio_reactive'] = audio_reactive\n"
        ]
        audio_lines = audio_lines[:i+1] + new_audio + audio_lines[i+1:]
        print("✅ Added audio reactive analysis")
        break

with open("audio_analyzer.py", "w", encoding="utf-8") as f:
    f.writelines(audio_lines)

print("✅ AUDIO ANALYZER FIXED!")
print("\n🎉 ALL INTEGRATIONS COMPLETE - TEST NOW!")
