with open("audio_analyzer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find where to insert audio reactive call (after "Deep Music Analysis Complete!")
insert_index = None
for i, line in enumerate(lines):
    if "Deep Music Analysis Complete!" in line:
        insert_index = i + 1
        break

if insert_index:
    # Insert audio reactive analysis
    new_lines = [
        "\n",
        "            # AUDIO REACTIVE EFFECTS\n",
        "            print('  🎛️ Audio Reactive Effects Analysis...')\n",
        "            audio_reactive = audio_reactive_engine.analyze_for_effects(audio_path, music_structure)\n",
        "            audio_data['audio_reactive'] = audio_reactive\n",
        "            print('  ✅ Audio reactive complete!')\n"
    ]
    
    lines = lines[:insert_index] + new_lines + lines[insert_index:]
    
    with open("audio_analyzer.py", "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("✅ Audio reactive ACTUALLY added this time!")
else:
    print("❌ Could not find insertion point")

# Now add segment quality to visual intelligence
with open("visual_intelligence_v2.py", "r", encoding="utf-8") as f:
    visual_lines = f.readlines()

# Find Claude call and add segment quality before it
for i, line in enumerate(visual_lines):
    if "GET ANALYSIS FROM CLAUDE" in line and "SEGMENT QUALITY" not in visual_lines[i-5:i]:
        visual_lines.insert(i, "        # SEGMENT QUALITY\n")
        visual_lines.insert(i+1, "        print('  🔍 Quality analysis...')\n")
        visual_lines.insert(i+2, "        segment_quality = segment_quality_analyzer.analyze_video_segments(video_path)\n")
        visual_lines.insert(i+3, "\n")
        break

with open("visual_intelligence_v2.py", "w", encoding="utf-8") as f:
    f.writelines(visual_lines)

print("✅ Segment quality call added!")

# Add to result
with open("visual_intelligence_v2.py", "r", encoding="utf-8") as f:
    content = f.read()

if "'segment_quality'" not in content:
    content = content.replace(
        "return result",
        "result['segment_quality'] = segment_quality\n        return result"
    )
    with open("visual_intelligence_v2.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Segment quality added to result!")

print("\n🎉 ALL FIXES APPLIED! Run program now!")
