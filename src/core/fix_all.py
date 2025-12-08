import re

print("🔧 FIXING ALL INTEGRATIONS...")

# 1. FIX AUDIO ANALYZER - Add audio reactive call
print("\n[1/3] Fixing audio analyzer...")
with open("audio_analyzer.py", "r", encoding="utf-8") as f:
    audio_content = f.read()

# Add audio reactive analysis after music structure
if "analyze_for_effects" not in audio_content:
    # Find where to insert (after music structure analysis)
    old = "print('? Deep Music Analysis Complete!')"
    new = """print('? Deep Music Analysis Complete!')
            
            # Audio Reactive Effects for superhuman sync
            print("  🎛️ Analyzing audio reactivity...")
            audio_reactive = audio_reactive_engine.analyze_for_effects(audio_path, music_structure)
            audio_data["audio_reactive"] = audio_reactive"""
    
    audio_content = audio_content.replace(old, new)
    
    with open("audio_analyzer.py", "w", encoding="utf-8") as f:
        f.write(audio_content)
    print("   ✅ Audio reactive analysis added")
else:
    print("   ✓ Audio reactive already integrated")

# 2. FIX VISUAL INTELLIGENCE - Add segment quality call  
print("\n[2/3] Fixing visual intelligence...")
with open("visual_intelligence_v2.py", "r", encoding="utf-8") as f:
    visual_content = f.read()

if "segment_quality_analyzer" not in visual_content:
    # Add import
    visual_content = visual_content.replace(
        "import anthropic",
        "import anthropic\nfrom .segment_quality_analyzer import segment_quality_analyzer"
    )
    
    # Add quality analysis before Claude call
    old_call = "# GET ANALYSIS FROM CLAUDE"
    new_call = """# SEGMENT QUALITY ANALYSIS
            print("  🔍 Analyzing segment quality...")
            segment_quality = segment_quality_analyzer.analyze_video_segments(video_path)
            
            # GET ANALYSIS FROM CLAUDE"""
    
    visual_content = visual_content.replace(old_call, new_call)
    
    # Add to result
    visual_content = visual_content.replace(
        "return result",
        "result['segment_quality'] = segment_quality\n        return result"
    )
    
    with open("visual_intelligence_v2.py", "w", encoding="utf-8") as f:
        f.write(visual_content)
    print("   ✅ Segment quality analysis added")
else:
    print("   ✓ Segment quality already integrated")

# 3. FIX CLAUDE DIRECTOR - Use quality data
print("\n[3/3] Fixing Claude Director...")
with open("claude_director.py", "r", encoding="utf-8") as f:
    director_content = f.read()

if "'quality':" not in director_content:
    # Add quality to compressed data
    old_append = """'duration': analysis.get('duration', 5.0)
            })"""
    
    new_append = """'duration': analysis.get('duration', 5.0),
                'quality': int(analysis.get('segment_quality', {}).get('average_quality', 70)),
                'best_segments': [f"{s['start']:.1f}-{s['end']:.1f}s" for s in analysis.get('segment_quality', {}).get('best_segments', [])[:2]]
            })"""
    
    director_content = director_content.replace(old_append, new_append)
    
    with open("claude_director.py", "w", encoding="utf-8") as f:
        f.write(director_content)
    print("   ✅ Quality data integrated into Claude Director")
else:
    print("   ✓ Quality data already in Claude Director")

print("\n✅ ALL FIXES COMPLETE!")
print("\nNEXT: Run the program and you'll see:")
print("  🔍 Quality analysis during import")
print("  🎛️ Audio reactive analysis during music analysis")
print("  📊 Claude Director using quality scores")
