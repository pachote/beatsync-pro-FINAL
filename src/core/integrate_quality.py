import re

with open("visual_intelligence_v2.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add import
if "segment_quality_analyzer" not in content:
    content = content.replace(
        "import anthropic",
        "import anthropic\nfrom .segment_quality_analyzer import segment_quality_analyzer"
    )

# Add quality analysis to analyze_video method
# Find where frames are extracted and add quality analysis after
old_analysis = """        # GET ANALYSIS FROM CLAUDE
        result = self._call_claude_vision(content)"""

new_analysis = """        # SEGMENT QUALITY ANALYSIS (finds best parts)
        print("  🔍 Analyzing segment quality...")
        segment_quality = segment_quality_analyzer.analyze_video_segments(video_path)
        
        # GET ANALYSIS FROM CLAUDE
        result = self._call_claude_vision(content)
        
        # Add segment quality to result
        result['segment_quality'] = segment_quality"""

content = content.replace(old_analysis, new_analysis)

with open("visual_intelligence_v2.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Segment quality integrated into visual analyzer!")
print("   Now analyzing best/worst parts of every clip")
