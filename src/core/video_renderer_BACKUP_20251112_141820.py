import sys
from pathlib import Path
import traceback

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Create a log file to capture errors
log_file = Path(__file__).parent.parent.parent / "import_debug.log"

try:
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("=== Starting effects import ===\n")
        f.write(f"sys.path: {sys.path}\n")
        f.write(f"Current file: {__file__}\n")
        f.write(f"Project root: {Path(__file__).parent.parent.parent}\n\n")
        f.flush()
        
        f.write("Importing ColorGradingEngine...\n")
        f.flush()
        from src.effects.color_grading_engine import ColorGradingEngine
        f.write("✓ ColorGradingEngine imported successfully\n")
        f.flush()
        
        f.write("Importing BeatReactiveEffects...\n")
        f.flush()
        from src.effects.beat_reactive_effects import BeatReactiveEffects
        f.write("✓ BeatReactiveEffects imported successfully\n")
        f.flush()
        
        f.write("Importing TransitionEffects...\n")
        f.flush()
        from src.effects.transition_effects import TransitionEffects
        f.write("✓ TransitionEffects imported successfully\n")
        f.flush()
        
        f.write("Importing CameraMotion...\n")
        f.flush()
        from src.effects.camera_motion import CameraMotion
        f.write("✓ CameraMotion imported successfully\n")
        f.flush()
        
        EFFECTS_AVAILABLE = True
        f.write("\n=== ALL IMPORTS SUCCESSFUL ===\n")
except Exception as e:
    EFFECTS_AVAILABLE = False
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n✗✗✗ IMPORT FAILED ✗✗✗\n")
        f.write(f"Error: {e}\n")
        f.write(f"Error type: {type(e).__name__}\n")
        f.write(f"\nFull traceback:\n")
        f.write(traceback.format_exc())
        f.write("\n=== END ERROR LOG ===\n")
"""
BeatSync PRO - GPU H.264 Renderer (FIXED v2)
Fixed bugs: absolute paths, NVENC fallback, disk space check, stream copy
"""

import subprocess
from .audio_analyzer import AudioAnalyzer
import os
import shutil
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from .transitions_engine import TransitionEngine, MusicEnergyAnalyzer
from .speed_variations import SpeedVariationEngine, MusicSectionDetector
from .smart_trimming import SmartTrimmingEngine, ContentAnalyzer


class VideoRenderer:
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.project_root = Path(__file__).parent.parent.parent  # Go up to project root
        print(f"? GPU H.264 Renderer initialized")
        print(f"   Project root: {self.project_root}")
        self.transition_engine = TransitionEngine()
        self.speed_engine = SpeedVariationEngine()
        self.audio_analyzer = AudioAnalyzer()
        self.trimming_engine = SmartTrimmingEngine()
        print("   ? Professional Transitions Engine loaded")
        print("   ? Speed Variations Engine loaded")
        print("   ??  Smart Trimming Engine loaded")

        # Initialize effects engines
        if EFFECTS_AVAILABLE:
            self.color_engine = ColorGradingEngine()
            self.camera_motion = CameraMotion()
            self.beat_effects = BeatReactiveEffects()
            self.transitions = TransitionEffects()
            print("   ?? Camera Motion Engine loaded")
            print("   ?? Color Grading Engine loaded")
        else:
            self.camera_motion = None
            self.color_engine = None
            print("   ??  Effects libraries not available")


    def apply_all_engines(self, clip_data, clip_index, music_duration, beat_times, previous_clip=None):
        """Apply all 3 engines to a clip"""
        current_time = clip_data.get('start_time', 0)
        duration = clip_data.get('duration', 2.0)
        
        # Calculate music energy (0-1)
        music_energy = MusicEnergyAnalyzer.get_music_energy(current_time, music_duration)
        
        # Calculate beat strength (0-1)
        beat_strength = MusicEnergyAnalyzer.get_beat_strength(beat_times, current_time)
        
        # Detect musical sections
        prev_energy = 0.5
        if previous_clip:
            prev_time = previous_clip.get('start_time', 0)
            prev_energy = MusicEnergyAnalyzer.get_music_energy(prev_time, music_duration)
        
        is_drop = MusicSectionDetector.is_drop(current_time, beat_times, music_energy)
        is_breakdown = MusicSectionDetector.is_breakdown(current_time, music_energy, prev_energy)
        
        # ENGINE 1: Smart Trimming
        trim_data = self.trimming_engine.select_trim_point(
            clip_data=clip_data,
            desired_duration=duration,
            music_energy=music_energy,
            previous_clip=previous_clip
        )
        
        
        # ENGINE 2: Speed Variations (DISABLED - focusing on precision)
        speed_data = {
            'speed': 1.0,
            'filter': None,
            'description': 'normal'
        }
        speed_data = self.speed_engine.select_speed(
        clip_index=clip_index,
        clip_data=clip_data,
        music_energy=music_energy,
        beat_strength=beat_strength,
        is_drop=is_drop,
        is_breakdown=is_breakdown
        )
        
        # Combine all engine data
        enhanced_clip = clip_data.copy()
        enhanced_clip['trim_start'] = trim_data['trim_start']
        enhanced_clip['speed'] = speed_data['speed']
        enhanced_clip['speed_filter'] = speed_data.get('filter')

        # DEBUG: Show what effects are being considered
        print(f"[CLIP {clip_index}] Checking effects:")
        print(f"   aesthetic_style={self.aesthetic_style}, effects_style={self.effects_style}")
        
        # Get camera motion filter for this clip
        camera_filter = self._get_effects_filter(enhanced_clip)
        if camera_filter:
            if 'effects' not in enhanced_clip:
                enhanced_clip['effects'] = {}
            enhanced_clip['effects']['camera_motion'] = camera_filter
        
        # Apply beat-reactive effects (glitch, flash, etc.)
        print(f"   Beat effects check: EFFECTS_AVAILABLE={EFFECTS_AVAILABLE}, has_beat_effects={self.beat_effects is not None}, style={self.effects_style}")
        if EFFECTS_AVAILABLE and self.beat_effects and self.effects_style != 'Clean':
            # Convert beat_strength (0-1) to energy_level (1-10)
            energy_level = int(beat_strength * 9) + 1
            beat_effect = self.beat_effects.get_energy_based_effect(energy_level)
            if beat_effect:
                enhanced_clip['effects']['beat_reactive'] = beat_effect
                print(f"   🎆 Beat effect applied: {self.effects_style}")
        
        return enhanced_clip

    def render_music_video(self, edit_plan, music_path, output_path):
        """Main entry point - matches GUI expectations"""
        clips = edit_plan.get('clips', [])
        aesthetic_style = edit_plan.get('color', 'Natural')  # UI uses 'color' key
        effects_style = edit_plan.get('effects', 'Clean')  # UI uses 'effects' key
        
        # Analyze audio for reactive effects
        print("\n  ?? Analyzing audio for reactive effects...")
        self.audio_data = self.audio_analyzer.analyze_music(music_path)
        print(f"  ? Audio analysis complete!")
        
        return self.render_video(clips, music_path, output_path, aesthetic_style, effects_style)

    def _get_effects_filter(self, clip: Dict) -> str:
        """Get camera motion filter based on effects preset"""
        if not EFFECTS_AVAILABLE or not self.camera_motion:
            return ''
        
        effects_style = self.effects_style
        duration = clip.get('duration', 2.0)
        
        # Skip camera effects for clips shorter than 1.5 seconds
        if duration < 1.5:
            return ''
        energy = clip.get('energy', 5)
        
        # Map effects preset to camera motion
        motion_map = {
            'Clean': 'static',
            'Subtle': ('ken_burns', 0.2),
            'Cinematic': ('ken_burns', 0.4),
            'Music Video': 'zoom_in' if energy >= 7 else 'static',
            'Experimental': 'shake',
            'Glitch': ('shake', 0.8),
            'Retro': ('pan_left', 0.3),
            'Glitch Storm': ('shake', 1.0)
        }
        
        motion = motion_map.get(effects_style, 'static')
        
        if motion == 'static':
            return ''
        
        # Handle tuple (motion_type, intensity)
        if isinstance(motion, tuple):
            motion_type, intensity = motion
            return self.camera_motion.get_motion_filter(motion_type, duration, intensity)
        else:
            return self.camera_motion.get_motion_filter(motion, duration, 0.5)
    
    def _apply_audio_reactive_effects(self, clip_dict: Dict, audio_reactive: Dict) -> Dict:
        """Apply audio-reactive effects (zoom, flash, speed) to clip"""
        if not audio_reactive:
            return clip_dict
        
        clip_start = clip_dict.get('start_time', 0)
        clip_end = clip_start + clip_dict.get('duration', 2.0)
        
        effects_filter = []
        
        # 1. ZOOM EVENTS - bass-reactive zoom pulses
        for zoom in audio_reactive.get('zoom_events', []):
            zoom_time = zoom['time']
            if clip_start <= zoom_time < clip_end:
                # Zoom pulse: 1.0 -> (1.0 + strength) -> 1.0
                strength = zoom.get('strength', 0.2)
                duration = zoom.get('duration', 0.1)
                
                # Calculate relative time in clip
                rel_time = zoom_time - clip_start
                
                # Zoom in and out over duration
                zoom_filter = f"zoompan=z='if(between(t,{rel_time},{rel_time+duration}),1+{strength}*(sin((t-{rel_time})*PI/{duration})),1)':d=1:s=1920x1080"
                effects_filter.append(zoom_filter)
                
                print(f"       ?? Zoom pulse @ {zoom_time:.2f}s (strength: {strength})")
        
        # 2. FLASH EVENTS - snare-reactive brightness
        for flash in audio_reactive.get('flash_events', []):
            flash_time = flash['time']
            if clip_start <= flash_time < clip_end:
                intensity = flash.get('intensity', 0.3)
                duration = flash.get('duration', 0.05)
                
                rel_time = flash_time - clip_start
                
                # Quick brightness flash
                flash_filter = f"eq=brightness='if(between(t,{rel_time},{rel_time+duration}),{intensity}*(1-abs((t-{rel_time}-{duration/2})*2/{duration})),0)'"
                effects_filter.append(flash_filter)
        
        # 3. SPEED VARIATIONS - buildups and drops
        for speed_var in audio_reactive.get('speed_variations', []):
            var_start = speed_var['start']
            var_end = speed_var['end']
            
            # Check if this clip overlaps with speed variation
            if not (clip_end < var_start or clip_start > var_end):
                start_speed = speed_var.get('start_speed', 1.0)
                end_speed = speed_var.get('end_speed', 1.0)
                var_type = speed_var.get('type', '')
                
                # Calculate speed at this clip's position
                if var_start <= clip_start <= var_end:
                    progress = (clip_start - var_start) / (var_end - var_start)
                    clip_speed = start_speed + (end_speed - start_speed) * progress
                    clip_dict['speed'] = round(clip_speed, 2)
                    print(f"       ? Speed: {clip_speed:.2f}x ({var_type})")
        
        # Combine effects into ffmpeg filter
        if effects_filter:
            existing_filter = clip_dict.get('effects', {}).get('ffmpeg_filter', '')
            combined = ','.join([f for f in [existing_filter] + effects_filter if f])
            clip_dict['effects']['ffmpeg_filter'] = combined
        
        return clip_dict

    def render_video(self, clips: List[Dict], music_path: str, output_path: str, aesthetic_style: str = "Modern", effects_style: str = "Clean"):
        """Render using GPU-accelerated H.264 with fallback"""
        
        # Store UI presets
        self.aesthetic_style = aesthetic_style
        self.effects_style = effects_style
        
        print(f"?? Effects loaded!")
        print(f"   Color Preset: {aesthetic_style}")
        print(f"   Effects Preset: {effects_style}")

        print("\n" + "=" * 60)
        print("?? FAST GPU RENDERER (FIXED)")
        print("=" * 60)
        print(f"   Total clips: {len(clips)}")
        print(f"   Output: {output_path}")
        print("")

        # FIX #1: Use absolute path for temp directory

        # Apply AI engines to all clips
        print("\n?? Applying AI Engines to clips...")
        enhanced_clips = []
        music_duration = 180.0  # Default, should get from audio analysis
        beat_times = []  # Should get from audio analysis
        
        for i, clip in enumerate(clips):
            previous = enhanced_clips[i-1] if i > 0 else None
            enhanced = self.apply_all_engines(clip, i, music_duration, beat_times, previous)
            
            enhanced_clips.append(enhanced)
            
            if i % 10 == 0:
                speed_desc = enhanced.get('speed', 1.0)
                print(f"  Clip {i+1}: {speed_desc}x speed")
        
        print(f"? Enhanced {len(enhanced_clips)} clips with AI engines")
        clips = enhanced_clips

        # FILTER OUT INVALID CLIPS (prevents black frames)
        print("  ?? Validating clips...")
        valid_clips = []
        for i, clip in enumerate(clips):
            if not clip.get('video_path'):
                print(f"  ??  Skipping clip {i+1}: missing video_path")
                continue
            video_path = clip['video_path']
            if not os.path.exists(video_path):
                print(f"  ??  Skipping clip {i+1}: file not found")
                continue
            valid_clips.append(clip)
        
        skipped = len(clips) - len(valid_clips)
        if skipped > 0:
            print(f"  ??  Removed {skipped} invalid clips")
        clips = valid_clips
        print(f"  ? Validated: {len(clips)} good clips")
        temp_dir = self.project_root / "output" / "temp_clips"
        temp_dir.mkdir(parents=True, exist_ok=True)
        print(f"   Temp dir: {temp_dir}")

        # FIX #2: Check disk space BEFORE rendering
        self._check_disk_space(temp_dir)

        try:
            self._update_progress("Rendering clips with GPU...", 0)
            clip_paths = self._render_clips_gpu(clips, temp_dir)

            self._update_progress("Assembling video...", 60)
            temp_video = temp_dir / "temp_video.mp4"
            self._concatenate_clips(clip_paths, temp_video)

            self._update_progress("Adding audio...", 80)
            self._add_audio(temp_video, music_path, output_path)

            self._update_progress("Cleaning up...", 95)
            self._cleanup(temp_dir)

            self._update_progress("Complete!", 100)
            print(f"\n? Video saved: {output_path}\n")

            return output_path

        except Exception as e:
            print(f"\n? Render error: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _check_disk_space(self, path: Path, required_gb=10):
        """Check if there's enough disk space"""
        stat = shutil.disk_usage(path.parent)
        free_gb = stat.free / (1024**3)
        
        print(f"   Disk space: {free_gb:.1f}GB free")
        
        if free_gb < required_gb:
            raise RuntimeError(
                f"Insufficient disk space: {free_gb:.1f}GB free, need at least {required_gb}GB\n"
                f"Please free up space on {path.drive} drive"
            )

    def _render_clips_gpu(self, clips: List[Dict], temp_dir: Path) -> List[Path]:
        """Render clips in parallel using GPU H.264"""

        print(f"?? Rendering {len(clips)} clips (GPU parallel)...\n")

        clip_paths = []
        total_clips = len(clips)

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}

            for i, clip in enumerate(clips):
                future = executor.submit(self._render_single_clip_gpu, i, clip, temp_dir)
                futures[future] = i

            for future in as_completed(futures):
                i = futures[future]
                try:
                    clip_path = future.result()
                    clip_paths.append((i, clip_path))

                    progress = int((len(clip_paths) / total_clips) * 60)
                    self._update_progress(f"Rendering clips ({len(clip_paths)}/{total_clips})...", progress)
                    print(f"  ? Clip {len(clip_paths)}/{total_clips} rendered")

                except Exception as e:
                    print(f"  ? Error rendering clip {i}: {e}")
                    raise

        clip_paths.sort(key=lambda x: x[0])
        return [path for _, path in clip_paths]

    def _render_single_clip_gpu(self, index: int, clip: Dict, temp_dir: Path) -> Path:
        """Render single clip with GPU acceleration and CPU fallback"""

        output_path = temp_dir / f"clip_{index:04d}.mp4"

        video_path = clip['video_path']
        trim_start = clip.get('trim_start', 0)
        duration = clip['duration']
        # Combine ALL effect filters
        filters = []
        
        # Camera motion filter (shake, zoom, etc.)
        camera_filter = clip.get('effects', {}).get('camera_motion', '')
        if camera_filter:
            filters.append(camera_filter)
            print(f"  [CLIP {index}] Camera filter: {camera_filter[:50]}")
        
        # Beat reactive filter (glitch, flash, etc.)
        beat_filter = clip.get('effects', {}).get('beat_reactive', '')
        if beat_filter:
            filters.append(beat_filter)
            print(f"  [CLIP {index}] Beat filter: {beat_filter[:50]}")
        
        # Color grading filter (cyberpunk, cinematic, etc.)
        color_filter = clip.get('effects', {}).get('color_grading', '')
        if color_filter:
            filters.append(color_filter)
            print(f"  [CLIP {index}] Color filter: {color_filter[:50]}")
        
        # Combine all filters
        effect_filter = ','.join(filters) if filters else ''
        
        # Apply speed variation from engines
        speed_filter = clip.get('speed_filter')
        
        # Combine all filters
        filters_to_apply = []
        if camera_filter:
            filters_to_apply.append(camera_filter)
        if speed_filter:
            filters_to_apply.append(speed_filter)
        if effect_filter:
            filters_to_apply.append(effect_filter)
        
        # Get color grading
        print(f"   Color check: EFFECTS_AVAILABLE={EFFECTS_AVAILABLE}, has_engine={self.color_engine is not None}, style={self.aesthetic_style}")
        if EFFECTS_AVAILABLE and self.color_engine and self.aesthetic_style != 'Natural':
            color_filter = self.color_engine.get_ffmpeg_filter(self.aesthetic_style)
            if color_filter:
                filters_to_apply.append(color_filter)
        
        # Combine all
        effect_filter = ','.join(filters_to_apply) if filters_to_apply else ''

        # DEBUG: Print what filters are being applied
        if filters_to_apply:
            print(f"  [CLIP {index}] Applying filters: {filters_to_apply}")
        if effect_filter:
            print(f"  [CLIP {index}] Final filter string: {effect_filter[:100]}")

        # DEBUG: Print what filters are being applied
        if filters_to_apply:
            print(f"  [CLIP {index}] Applying filters: {filters_to_apply}")
        if effect_filter:
            print(f"  [CLIP {index}] Final filter string: {effect_filter[:100]}")
# FIX #3: Try NVENC first, fallback to CPU if it fails
        try:
            return self._render_clip_nvenc(video_path, trim_start, duration, effect_filter, output_path)
        except subprocess.CalledProcessError as e:
            print(f"  ??  NVENC failed for clip {index}, falling back to CPU...")
            return self._render_clip_cpu(video_path, trim_start, duration, effect_filter, output_path)

    def _render_clip_nvenc(self, video_path, trim_start, duration, effect_filter, output_path):
        """Render with NVENC (GPU)"""
        
        cmd = [
            'ffmpeg',
            '-ss', str(trim_start),
            '-i', video_path,
            '-t', str(duration),
            '-c:v', 'h264_nvenc', '-movflags', '+faststart',
            '-preset', 'p4',
            '-rc', 'vbr',
            '-cq', '23',
            '-b:v', '15M',
            '-maxrate', '20M',
            '-bufsize', '30M',
            '-pix_fmt', 'yuv420p',
            '-r', '30'
        ]

        if effect_filter:
            cmd.extend(['-vf', effect_filter])

        cmd.extend(['-an', '-y', str(output_path)])

        # FIX #4: Show FFmpeg output for debugging
        result = subprocess.run(cmd, check=True, capture_output=True, timeout=180)
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr.decode()}")
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)

        return output_path

    def _render_clip_cpu(self, video_path, trim_start, duration, effect_filter, output_path):
        """Render with CPU (libx264) as fallback"""
        
        cmd = [
            'ffmpeg',
            '-ss', str(trim_start),
            '-i', video_path,
            '-t', str(duration),
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-r', '30'
        ]

        if effect_filter:
            cmd.extend(['-vf', effect_filter])

        cmd.extend(['-an', '-y', str(output_path)])

        subprocess.run(cmd, check=True, capture_output=True, timeout=3600)

        return output_path

    def _concatenate_clips(self, clip_paths: List[Path], output_path: Path):
        """Concatenate clips"""

        print(f"\n?? Concatenating {len(clip_paths)} clips...")

        concat_file = output_path.parent / "concat_list.txt"
        with open(concat_file, 'w') as f:
            for clip_path in clip_paths:
                f.write(f"file '{clip_path.absolute()}'\n")

        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30', '-y', str(output_path)
        ]

        result = subprocess.run(cmd, check=True, capture_output=True, timeout=3600)
        
        if result.returncode != 0:
            print(f"FFmpeg concat error: {result.stderr.decode()}")
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
            
        print(f"  ? Concatenation complete")

    def _add_audio(self, video_path: Path, music_path: str, output_path: str):
        """Add audio to video"""

        print(f"\n?? Adding audio...")

        # FIX #5: Use stream copy instead of re-encoding
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-i', music_path,
            '-map', '0:v:0',  # FIX: Map video from input 0
            '-map', '1:a:0',  # FIX: Map audio from input 1
            '-c:v', 'copy',  # FIX: Stream copy instead of re-encode
            '-c:a', 'aac',
            '-b:a', '320k',
            '-shortest',
            '-y', output_path
        ]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, timeout=3600)
            
            if result.returncode != 0:
                print(f"FFmpeg audio error: {result.stderr.decode()}")
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                
            print(f"  ? Audio added")
            
        except subprocess.CalledProcessError as e:
            print(f"\n? FFmpeg failed with error code {e.returncode}")
            if e.stderr:
                print(f"Error output: {e.stderr.decode()}")
            raise RuntimeError(f"Failed to add audio: {e}")

    def _cleanup(self, temp_dir: Path):
        """Clean up temp files"""
        import shutil
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
                print(f"  ? Cleaned up temp files")
            except Exception as e:
                print(f"  ??  Could not cleanup temp dir: {e}")

    def _update_progress(self, message: str, percent: int):
        """Update progress"""
        print(f"  [{percent}%] {message}")
        if self.progress_callback:
            self.progress_callback(message, percent)


























