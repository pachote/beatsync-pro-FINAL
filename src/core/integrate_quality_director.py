import re

with open("claude_director.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add segment quality to compressed clip data
old_compress = """def _compress_clip_data(self, video_analyses):
        \"\"\"Compress clip analysis for token efficiency - supports 300+ clips\"\"\"
        compressed = []
        for clip_id, analysis in video_analyses.items():"""

new_compress = """def _compress_clip_data(self, video_analyses):
        \"\"\"Compress clip analysis for token efficiency - supports 300+ clips\"\"\"
        compressed = []
        for clip_id, analysis in video_analyses.items():
            # Get segment quality data
            segment_quality = analysis.get('segment_quality', {})
            best_segments = segment_quality.get('best_segments', [])
            skip_segments = segment_quality.get('skip_segments', [])
            avg_quality = segment_quality.get('average_quality', 70)"""

content = content.replace(old_compress, new_compress)

# Add quality info to compressed data
old_append = """compressed.append({
                'id': clip_id,
                'subject': analysis.get('subject_type', 'unknown'),
                'style': analysis.get('art_style', 'unknown'),
                'energy': analysis.get('energy_level', 5),
                'motion': analysis.get('motion_intensity', 'medium'),
                'lip_sync': analysis.get('lip_sync_suitable', False),
                'duration': analysis.get('duration', 5.0)
            })"""

new_append = """compressed.append({
                'id': clip_id,
                'subject': analysis.get('subject_type', 'unknown'),
                'style': analysis.get('art_style', 'unknown'),
                'energy': analysis.get('energy_level', 5),
                'motion': analysis.get('motion_intensity', 'medium'),
                'lip_sync': analysis.get('lip_sync_suitable', False),
                'duration': analysis.get('duration', 5.0),
                'quality': int(avg_quality),
                'best_segments': [f"{s['start']:.1f}-{s['end']:.1f}s (Q:{s['quality']})" for s in best_segments[:3]],
                'skip_segments': [f"{s['start']:.1f}-{s['end']:.1f}s ({s['reason']})" for s in skip_segments[:2]]
            })"""

content = content.replace(old_append, new_append)

# Add quality intelligence to prompt
old_prompt_section = """MUSICAL SECTIONS GUIDE:"""

new_prompt_section = """QUALITY INTELLIGENCE:
Each clip has segment-level quality scores (0-100). Use ONLY the best segments:
- Quality 85+: PERFECT for key moments (drops, vocals, hero shots)
- Quality 70-84: Good for normal sections
- Quality 50-69: Use sparingly, only if needed
- Quality <50: AVOID (morphing/glitches detected)

Example clip data:
  Clip 12: Quality 92, Best: 0-2s(Q:95), 4-6s(Q:98), Skip: 2-4s(morphing)
  → Use 0-2s for intro, 4-6s for drop, SKIP 2-4s

INTELLIGENT CLIP REUSE:
You can use the SAME clip multiple times with different segments:
- Clip 5: Use 0-2s at 10s, use 4-6s at 60s (different moments)
- This creates callbacks and maximizes quality

MUSICAL SECTIONS GUIDE:"""

content = content.replace(old_prompt_section, new_prompt_section)

with open("claude_director.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Claude Director now has quality intelligence!")
