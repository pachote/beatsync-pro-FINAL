import re

with open("claude_director.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add music intelligence prompt builder method
music_intelligence_method = """
    def _build_music_intelligence_prompt(self, music_structure) -> str:
        \"\"\"Build prompt section with music intelligence\"\"\"
        if not music_structure:
            return "No music structure analysis available."
        
        prompt = []
        prompt.append(f"Duration: {music_structure['duration']:.1f}s")
        
        # Drops
        if music_structure['drops']:
            prompt.append(f"\\n💥 DROPS ({len(music_structure['drops'])} detected) - Use MOST DRAMATIC clips with MAXIMUM effects:")
            for drop in music_structure['drops'][:10]:
                prompt.append(f"   - {drop}s: MASSIVE EFFECT MOMENT")
        
        # Buildups
        if music_structure['buildups']:
            prompt.append(f"\\n📈 BUILDUPS ({len(music_structure['buildups'])} detected) - Progressively increase intensity:")
            for start, end in music_structure['buildups'][:5]:
                prompt.append(f"   - {start}s-{end}s: Ramp from calm to intense")
        
        # Vocal segments
        if music_structure['vocal_segments']:
            prompt.append(f"\\n🎤 VOCALS ({len(music_structure['vocal_segments'])} segments) - Use ONLY lip-sync suitable clips:")
            for start, end in music_structure['vocal_segments'][:5]:
                prompt.append(f"   - {start}s-{end}s: LIP-SYNC CLIPS ONLY")
        
        # Sections
        prompt.append(f"\\n🎼 SECTIONS ({len(music_structure['sections'])}):")
        for section in music_structure['sections']:
            desc = f"   - {section['start']:.0f}-{section['end']:.0f}s: {section['type'].upper()} (energy: {section['energy']:.2f})"
            if section['has_vocals']:
                desc += " 🎤"
            if section['has_drop']:
                desc += " 💥"
            prompt.append(desc)
        
        return "\\n".join(prompt)
"""

# Find where to insert the method (before _create_enhanced_prompt)
if "_build_music_intelligence_prompt" not in content:
    content = content.replace("    def _create_enhanced_prompt(", music_intelligence_method + "\n    def _create_enhanced_prompt(")

# Add music structure to music_data
if "'music_structure':" not in content:
    content = content.replace(
        "music_data = {",
        "music_data = {\n            'music_structure': audio_data.get('music_structure', None),"
    )

# Add music intelligence to prompt
if "MUSIC INTELLIGENCE ANALYSIS" not in content:
    content = content.replace(
        "You are an expert AI video editor",
        "You are an AGI-level video editor with superhuman music understanding.\n\n**MUSIC INTELLIGENCE ANALYSIS:**\n{music_intelligence_prompt}\n\nYou are an expert AI video editor"
    )

# Add music intelligence prompt building
if "music_intelligence_prompt = self._build" not in content:
    content = content.replace(
        "user_vision_instruction = {",
        "# Build music intelligence section\n        music_intelligence_prompt = self._build_music_intelligence_prompt(music_data.get('music_structure'))\n        \n        user_vision_instruction = {"
    )

# Add to format call
if "music_intelligence_prompt=" not in content:
    content = content.replace(
        "prompt = prompt_template.format(",
        "prompt = prompt_template.format(music_intelligence_prompt=music_intelligence_prompt, "
    )

with open("claude_director.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Claude Director patched with music intelligence!")
