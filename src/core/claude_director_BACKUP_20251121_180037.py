import logging
logger = logging.getLogger(__name__)

"""
BeatSync PRO v15 - Phase 4: MULTI-PASS AI REFINEMENT
Claude reviews and optimizes its own editing decisions
"""

import anthropic
import base64
import json
from pathlib import Path
import cv2
import traceback

from core.editing_presets import EditingPreset
from core.face_detector import FaceDetector

class ClaudeAIDirector:
    def __init__(self, api_key=None):
        if api_key:
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            import os
            self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        self.recent_clips = []
        self.face_detector = FaceDetector()
        print("✅ Claude Director initialized - Phase 4: Multi-Pass Refinement")
        print(f"   Model: {self.model}")
        
    def analyze_clips(self, video_files):
        """Analyze clips with COMPLETE professional intelligence"""
        clips_data = []
        
        analysis_system_prompt = """You are a world-class music video editor with perfect musical and cinematic intuition.

FOR EACH CLIP, PROVIDE COMPREHENSIVE JSON ANALYSIS:

{
  "basic_attributes": {
    "subject_type": "person/object/scene/abstract/nature/architecture/action",
    "art_style": "realistic/animated/stylized/abstract/cinematic/artistic",
    "dominant_colors": "warm/cool/vibrant/muted/monochrome/neon",
    "lighting": "bright/dark/dramatic/natural/neon/moody",
    "camera_movement": "static/slow_pan/fast/shaky/smooth/zoom",
    "composition": "close_up/medium/wide/extreme_wide/abstract"
  },
  "professional_intelligence": {
    "visual_complexity": 5,
    "emotional_tone": "calm/happy/energetic/intense/mysterious/melancholic/aggressive/peaceful",
    "action_content": "static/subtle/moderate/fast/frenetic/explosive",
    "energy_level": 7,
    "narrative_potential": 6,
    "standout_factor": 8,
    "viewer_attention_grab": 7
  },
  "trimming_intelligence": {
    "best_moment_location": "middle",
    "peak_visual_timing": "3-6",
    "avoid_these_parts": ["boring intro", "slow end"],
    "minimum_effective_duration": 0.5,
    "maximum_effective_duration": 8.0,
    "optimal_trim_start": 2.0,
    "optimal_trim_end": 5.0
  },
  "musical_context": {
    "best_for_sections": ["verse", "chorus", "drop"],
    "best_for_beat_types": ["kick", "snare", "hi-hat"],
    "ideal_duration_range": "2-4",
    "energy_compatibility": 7,
    "works_in_sequence_with": ["similar subject types"],
    "creates_contrast_with": ["opposite energy clips"]
  },
  "clip_personality": {
    "mood": "energetic",
    "visual_impact": "strong",
    "pacing_contribution": "speeds_up",
    "storytelling_role": "action",
    "reusability": "callback_potential"
  }
}

CRITICAL: Return ONLY valid JSON. No markdown, no explanations, just the JSON object.
Use actual values like numbers and specific strings, not placeholders."""
        
        for video_path in video_files:
            try:
                print(f"Analyzing {Path(video_path).name} with ULTIMATE intelligence...")
                frames = self._extract_frames(video_path)
                analysis = self._analyze_frames_with_claude(frames, analysis_system_prompt)
                clips_data.append({'path': video_path, 'analysis': analysis, 'filename': Path(video_path).name})
                
                prof = analysis.get('professional_intelligence', {})
                pers = analysis.get('clip_personality', {})
                print(f"✓ Energy: {prof.get('energy_level', 5)}/10 | Mood: {pers.get('mood', 'neutral')}")
            except Exception as e:
                logger.exception("Claude API call failed")
                clips_data.append({
                    'path': video_path,
                    'analysis': self._get_fallback_analysis(),
                    'filename': Path(video_path).name
                })
        
        return clips_data
    
    def create_edit_sequence(self, clips_data, beats_data, song_analysis):
        """Create edit with MULTI-PASS REFINEMENT"""
        
        print("\n🎬 PHASE 4: Multi-Pass AI Refinement")
        print("   Pass 1: Initial creative edit...")
        
        # PASS 1: Initial Edit
        initial_decisions = self._create_initial_edit(clips_data, beats_data, song_analysis)
        
        if not initial_decisions or len(initial_decisions) < 10:
            print("   ❌ Initial edit failed, using fallback")
            return initial_decisions
        
        print(f"   ✅ Initial edit: {len(initial_decisions)} clips")
        
        # PASS 2: Self-Review and Refinement
        print("   Pass 2: AI self-review and optimization...")
        refined_decisions = self._refine_edit_decisions(initial_decisions, clips_data, beats_data, song_analysis)
        
        if refined_decisions and len(refined_decisions) > 0:
            print(f"   ✅ Refined edit: {len(refined_decisions)} clips")
            print("   🎯 Multi-pass refinement complete!")
            
            # Update recent clips memory
            used_indices = [d.get('clip_index') for d in refined_decisions if d.get('clip_index') is not None]
            self.recent_clips.extend(used_indices[-20:])
            self.recent_clips = self.recent_clips[-20:]
            
            return refined_decisions
        else:
            print("   ⚠️ Refinement pass failed, using initial edit")
            return initial_decisions
    
    def _create_initial_edit(self, clips_data, beats_data, song_analysis):
        """PASS 1: Create initial edit sequence"""
        
        # Calculate song duration and estimate needed clips
        import math
        song_duration = song_analysis.get("duration", 0)
        if song_duration == 0 and beats_data:
            song_duration = max(beat["time"] for beat in beats_data) + 5
        estimated_clips = math.ceil(song_duration / 4.0)  # DYNAMIC: 60 clips
        print(f"   📊 SONG: {song_duration:.1f}s | NEED: ~{estimated_clips} clips")
        
        editing_system_prompt = """You are a MASTER music video editor creating a compelling visual masterpiece.

⚠️ CRITICAL REQUIREMENT - FULL SONG COVERAGE:
This song is {song_duration:.1f} seconds long.
You MUST create clips spanning from 0.0 seconds to {song_duration:.1f} seconds.


🎯 CRITICAL EDITING RULES FOR GENIUS-LEVEL RESULTS:

1. SYNCOPATION IS MANDATORY (30% of cuts):
   - Cut on the "+" between beats (off-beat)
   - Create unexpected rhythms
   - NEVER cut predictably on every beat!

2. DURATION CHAOS:
   - Never use same duration twice in a row
   - Pattern: 2s, 5s, 1s, 3s, 6s, 2s... (UNPREDICTABLE!)
   - Create tension through duration variation

3. ENERGY MATCHING:
   - High energy clips (8-10) = 1-2 seconds MAX
   - Medium energy (5-7) = 2-4 seconds
   - Low energy (1-4) = 4-6 seconds
   
4. BEAT TYPE STRATEGIES:
   - KICKS: Explosive 1-2s clips, skip every other kick
   - SNARES: Quick 2-3s transitions
   - HI-HATS: Let clips breathe 3-5s, don't cut every hi-hat

5. PATTERN BREAKING:
   - After 3 similar durations → BREAK THE PATTERN
   - After 4 on-beat cuts → OFF-BEAT cut
   - Create surprise without chaos!
Generate approximately {estimated_clips} clips with EXTREME VARIATION:
- High energy moments (chorus/drop): 1-2 seconds (RAPID FIRE!)
- Medium energy (verse): 2-4 seconds
- Low energy (intro/bridge): 4-6 seconds
CREATE VISUAL CHAOS through unpredictable cut timing!
The LAST clip must end at or very near {song_duration:.1f} seconds.
If you stop before the song ends, the video will be INCOMPLETE!

YOUR REVOLUTIONARY CAPABILITIES:
✓ Deep musical structure understanding
✓ Professional cinematic editing principles
✓ Memory of recent clips (avoid repetition)
✓ Energy curve matching
✓ Beat type classification
✓ Clip relationship understanding
✓ Strategic clip recycling
✓ Section-specific selection

🎯 CRITICAL EDITING RULES - BEAT-SYNCHRONIZED PRECISION:

1. KICK BEATS (bass drops):
   - Use HIGHEST energy clips (Energy 8-10/10)
   - Cut EXACTLY on the kick
   - Duration: 2-4 seconds (short, impactful)
   - Look for: explosive, impact_cuts style clips

2. SNARE BEATS (accents):
   - Change clips ON the snare hit
   - Use for transitions between different energy levels
   - Duration: 3-5 seconds
   - Create visual rhythm with snare pattern

3. HI-HAT PATTERNS (groove):
   - Longer clips that breathe (5-8 seconds)
   - Let the clip play out over multiple hi-hats
   - Use rhythmic_flow style clips
   - Build sustained energy

4. DYNAMIC VARIETY:
   - NO monotonous pacing - vary durations wildly
   - Alternate: short explosive clip → longer flowing clip → medium transition clip
   - Energy should MATCH beat intensity exactly
   - High energy moments = high energy clips, low moments = atmospheric clips

5. MUSICAL SECTIONS:
   - Intro/Outro: Atmospheric, longer clips (6-8s)
   - Verse: Steady rhythm, medium clips (4-6s)
   - Build-up: Increasing energy, decreasing durations (6s→5s→4s→3s)
   - Chorus: Maximum energy, rapid cuts on beats (2-4s)
   - Bridge: Contrast and variety

6. FLASH CUT STRATEGY (CRITICAL):
   - Chorus/Drop: Use 3-5 flash cuts (0.5-1.5s) per section
   - Beat drops: INSTANT flash cut on the drop (0.5-1s)
   - Build-ups: Accelerate towards drop (3s → 2s → 1s → 0.5s)
   - Kick hits: Random flash cuts (30% of kicks = 0.8-1.2s clips)
   
   Pattern example for chorus:
   [4s] [1s] [3s] [0.8s] [2s] [1.2s] [5s] [0.5s] [3s]
   ↑      ↑FLASH    ↑FLASH        ↑FLASH   ↑FLASH
   
   This creates IMPOSSIBLE-TO-COORDINATE human speed!

⚠️ CLIP REUSE RULES (PREVENT BORING REPETITION):
- NEVER reuse the same clip within 30 seconds of its last use
- Spread clip reuse evenly across the song
- Use ALL available clips before repeating ANY clip
- When forced to repeat, pick clips used longest ago
- Avoid creating predictable reuse patterns

🎯 SECTION UNIQUENESS (CRITICAL - PREVENT BORING VERSE/CHORUS REPEATS):
- Verse 1 clips ≠ Verse 2 clips (use DIFFERENT videos!)
- Chorus 1 clips ≠ Chorus 2 clips (VARY the selection!)
- Each similar section MUST feel unique
- Track which clips used in each section type
- Mix up the order - don't repeat patterns!

Example:
  Verse 1: Uses clips A, B, C, D, E
  Verse 2: MUST use clips F, G, H, I, J (NOT A, B, C again!)
  
This prevents "I've seen this before" feeling!



Your edit should feel IMPOSSIBLY precise, like a human couldn't coordinate it!

MUSICAL STRUCTURE:
{song_structure}

AVAILABLE CLIPS:
{clips_info}

RECENTLY USED CLIPS (AVOID):
{recent_clips}

CREATE YOUR INITIAL EDIT:

RETURN JSON:
{{
  "edit_decisions": [
    {{
      "time": 0.0,
      "clip_index": 0,
      "duration": 3.5,
      "trim_start": 2.0,
      "trim_end": 5.5,
      "beat_type": "kick",
      "musical_section": "intro",
      "reasoning": "Why this clip and timing"
    }}
  ],
  "creative_vision": "Brief description of the editing approach and story"
}}

CRITICAL: Return ONLY valid JSON, no markdown."""
        
        song_structure = self._format_song_structure(beats_data, song_analysis)
        clips_info = self._format_clips_for_decision(clips_data)
        recent_clips = self._format_recent_clips()
        
        full_prompt = editing_system_prompt.format(
            song_duration=song_duration,
            estimated_clips=estimated_clips,
            song_structure=song_structure,
            clips_info=clips_info,
            recent_clips=recent_clips
        )
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                messages=[{"role": "user", "content": full_prompt}]
            )
            
            return self._parse_edit_decisions(response.content[0].text)
        except Exception as e:
            print(f"   ❌ Error in initial edit: {e}")
            return []
    
    def _refine_edit_decisions(self, initial_decisions, clips_data, beats_data, song_analysis):
        """PASS 2: Review and refine the initial edit"""
        
        # Calculate coverage info for refinement
        song_duration = song_analysis.get("duration", 0)
        if song_duration == 0 and beats_data:
            song_duration = max(beat["time"] for beat in beats_data) + 5
        
        refinement_prompt = """You are a SENIOR EDITOR reviewing a music video edit for quality control.

🎯 VARIETY CHECK (CRITICAL):
- Check for repeated verse/chorus patterns
- Ensure each similar section uses different clips
- Verify 30-second minimum spacing on clip reuse
- No boring predictable sequences!
- Maximum unpredictability while maintaining quality


⚡ CRITICAL: PRESERVE FLASH CUTS!
DO NOT remove clips shorter than 2 seconds - they are INTENTIONAL flash cuts!
Flash cuts (0.5-1.5s) create the AGI genius feeling.
Only fix actual errors, keep the speed variation!


⚠️ CRITICAL - MAINTAIN FULL SONG COVERAGE:
This song is {song_duration:.1f} seconds long.
The edit MUST cover from 0.0s to {song_duration:.1f}s.
When refining, you can swap clips, adjust durations, improve transitions...
BUT you CANNOT reduce total coverage! The last clip must end near {song_duration:.1f}s.

ORIGINAL EDIT PLAN:
{initial_edit}

AVAILABLE CLIPS DATA:
{clips_summary}

SONG STRUCTURE:
{song_structure}

YOUR MISSION: Review this edit and identify improvements.

QUALITY CHECKS:
1. VARIETY: Are clips repeating too often? Same clip used within 10 clips?
2. ENERGY FLOW: Does energy build properly? Drops hit hard enough?
3. PACING: Are durations varied enough? Too many same-length clips?
4. COHERENCE: Do clips flow together? Or too random/jarring?
5. MUSICAL SYNC: Are key moments (bass drops, peaks) getting best clips?
6. NARRATIVE: Does it tell a story? Or just random visuals?
7. CLIP UTILIZATION: Are the BEST clips used in the BEST moments?
8. BORING SECTIONS: Any dull or low-energy sections that need fixing?

ANALYZE THE EDIT:
- What works well?
- What needs improvement?
- Which clips should be swapped?
- Should any durations change?
- Better flow/transitions possible?

RETURN IMPROVED EDIT:
{{
  "improvements_made": [
    "Specific improvement 1",
    "Specific improvement 2"
  ],
  "edit_decisions": [
    {{
      "time": 0.0,
      "clip_index": 0,
      "duration": 3.5,
      "trim_start": 2.0,
      "trim_end": 5.5,
      "beat_type": "kick",
      "musical_section": "intro",
      "reasoning": "Why this is better than original"
    }}
  ],
  "quality_score": 85
}}

MAKE IT BETTER! Return ONLY valid JSON."""
        
        # Format initial edit for review
        initial_edit_text = self._format_decisions_for_review(initial_decisions)
        clips_summary = self._format_clips_summary(clips_data)
        song_structure = self._format_song_structure(beats_data, song_analysis)
        
        full_prompt = refinement_prompt.format(
            song_duration=song_duration,
            initial_edit=initial_edit_text,
            clips_summary=clips_summary,
            song_structure=song_structure
        )
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                messages=[{"role": "user", "content": full_prompt}]
            )
            
            result = self._parse_refinement_response(response.content[0].text)
            
            if result and 'improvements_made' in result:
                print(f"\n   🎯 IMPROVEMENTS MADE:")
                for improvement in result.get('improvements_made', [])[:3]:
                    print(f"      • {improvement}")
                
                quality = result.get('quality_score', 0)
                print(f"   📊 Quality Score: {quality}/100")
            
            return result.get('edit_decisions', initial_decisions)
            
        except Exception as e:
            print(f"   ❌ Refinement error: {e}")
            return initial_decisions
    
    def _format_decisions_for_review(self, decisions):
        """Format edit decisions for review"""
        text = "EDIT SEQUENCE:\n"
        for i, d in enumerate(decisions[:20]):  # First 20 for review
            text += f"\n{i+1}. Time {d.get('time', 0):.1f}s: Clip {d.get('clip_index', 0)} for {d.get('duration', 2):.2f}s"
            text += f"\n   Trim: {d.get('trim_start', 0):.1f}-{d.get('trim_end', 5):.1f}s"
            text += f"\n   Section: {d.get('musical_section', 'unknown')}"
        
        if len(decisions) > 20:
            text += f"\n\n... ({len(decisions) - 20} more clips)"
        
        return text
    
    def _format_clips_summary(self, clips_data):
        """Brief summary of available clips"""
        text = "\nAVAILABLE CLIPS SUMMARY:\n"
        for i, clip in enumerate(clips_data[:15]):  # First 15
            a = clip.get('analysis', {})
            prof = a.get('professional_intelligence', {})
            basic = a.get('basic_attributes', {})
            text += f"{i}. {basic.get('subject_type', '?')} - Energy {prof.get('energy_level', 5)}/10\n"
        
        if len(clips_data) > 15:
            text += f"... ({len(clips_data) - 15} more clips)\n"
        
        return text
    
    def _parse_refinement_response(self, response_text):
        """Parse the refinement response"""
        try:
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                json_text = response_text.split("```")[1].split("```")[0]
            else:
                json_text = response_text
            
            return json.loads(json_text.strip())
        except Exception as e:
            print(f"      ❌ Refinement parse error: {e}")
            return None
    
    def _extract_frames(self, video_path, num_frames=5):
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Cannot open: {video_path}")
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = [int(total_frames * i / (num_frames + 1)) for i in range(1, num_frames + 1)]
        frames = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                frames.append(base64.b64encode(buffer).decode('utf-8'))
        cap.release()
        return frames
    
    def _analyze_frames_with_claude(self, frames, system_prompt):
        content = [{"type": "text", "text": "Analyze these frames with complete professional intelligence."}]
        for frame_b64 in frames:
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": frame_b64}})
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=system_prompt,
            messages=[{"role": "user", "content": content}]
        )
        
        try:
            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except:
            return self._get_fallback_analysis()
    
    def _get_fallback_analysis(self):
        return {
            "basic_attributes": {"subject_type": "abstract", "art_style": "cinematic", "dominant_colors": "vibrant", "lighting": "dramatic", "camera_movement": "smooth", "composition": "medium"},
            "professional_intelligence": {"visual_complexity": 6, "emotional_tone": "energetic", "action_content": "moderate", "energy_level": 6, "narrative_potential": 5, "standout_factor": 6, "viewer_attention_grab": 6},
            "trimming_intelligence": {"best_moment_location": "middle", "peak_visual_timing": "3-6", "avoid_these_parts": [], "minimum_effective_duration": 1.0, "maximum_effective_duration": 6.0, "optimal_trim_start": 2.0, "optimal_trim_end": 5.0},
            "musical_context": {"best_for_sections": ["verse", "chorus"], "best_for_beat_types": ["kick", "snare"], "ideal_duration_range": "2-4", "energy_compatibility": 6, "works_in_sequence_with": ["similar"], "creates_contrast_with": ["different"]},
            "clip_personality": {"mood": "neutral", "visual_impact": "moderate", "pacing_contribution": "maintains", "storytelling_role": "action", "reusability": "one_time"}
        }
    
    def _format_song_structure(self, beats_data, song_analysis):
        bpm = song_analysis.get('bpm', 120)
        duration = song_analysis.get('duration', 0)
        
        # Count beat types
        kicks = sum(1 for b in beats_data if b.get('beat_type') == 'kick')
        snares = sum(1 for b in beats_data if b.get('beat_type') == 'snare')
        hihats = sum(1 for b in beats_data if b.get('beat_type') == 'hi-hat')
        
        # Format beat list with types and timestamps
        beat_list = []
        for i, beat in enumerate(beats_data[:50]):  # First 50 beats for detail
            t = beat['time']
            bt = beat.get('beat_type', 'unknown')
            beat_list.append(f"{t:.1f}s ({bt})")
        
        result = f"""SONG STRUCTURE:
Duration: {duration:.1f}s @ {bpm:.1f} BPM
Total Beats: {len(beats_data)}
Beat Types: {kicks} kicks | {snares} snares | {hihats} hi-hats

KEY BEATS (first 50):
{', '.join(beat_list)}

EDITING STRATEGY:
- KICKS (bass drops): Use high-energy explosive clips, impact cuts
- SNARES (accents): Quick cuts, energy changes, clip transitions
- HI-HATS (groove): Rhythmic flow, maintain energy, subtle variations

Match clip energy to beat intensity. Use beat types for sophisticated timing!"""
        
        return result
    
    def _format_clips_for_decision(self, clips_data):
        text = "\n=== CLIPS ===\n"
        for i, clip in enumerate(clips_data[:10]):
            a = clip['analysis']
            prof = a.get('professional_intelligence', {})
            text += f"CLIP {i}: Energy {prof.get('energy_level', 5)}/10\n"
        return text
    
    def _format_recent_clips(self):
        if not self.recent_clips:
            return "None - first pass"
        return f"Recently used: {self.recent_clips}"
    
    def _parse_edit_decisions(self, response_text):
        try:
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                json_text = response_text.split("```")[1].split("```")[0]
            else:
                json_text = response_text
            
            data = json.loads(json_text.strip())
            return data.get('edit_decisions', [])
        except Exception as e:
            print(f"✗ Parse error: {e}")
            return []
    def create_edit_plan(self, video_analyses, music_analysis, user_config):
        """Bridge method for ai_tab.py"""
        print("Phase 4: Multi-Pass AI Refinement")
        clips_data = []
        for video_path, analysis in video_analyses.items():
            clips_data.append({'path': video_path, 'analysis': analysis, 'filename': video_path.split('/')[-1]})
        beats_data = music_analysis.get('beats', [])
        song_analysis = {'bpm': music_analysis.get('tempo', 120), 'duration': music_analysis.get('duration', 0), 'instruments': music_analysis.get('instruments', {}), 'emotions': music_analysis.get('emotions', {}), 'vocals': music_analysis.get('vocals', {}), 'sections': music_analysis.get('sections', [])}
        decisions = self.create_edit_sequence(clips_data, beats_data, song_analysis)
        converted_clips = []
        for decision in decisions:
            clip_index = decision.get('clip_index', 0)
            video_path = clips_data[clip_index]['path'] if 0 <= clip_index < len(clips_data) else clips_data[0]['path']
            converted_clips.append({'video_path': video_path, 'start_time': decision.get('time', 0), 'duration': decision.get('duration', 2.0), 'trim_start': decision.get('trim_start', 0), 'trim_end': decision.get('trim_end', 5.0), 'effects': {'ffmpeg_filter': '', 'creative_reasoning': decision.get('reasoning', 'AI clip'), 'intensity': 0.3}})
        print(f"Converted {len(converted_clips)} clips")
        return {'clips': converted_clips}
