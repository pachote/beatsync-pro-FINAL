# Video Generation Worker Thread
from PySide6.QtCore import QThread, Signal
from pathlib import Path

class VideoGenerationWorker(QThread):
    """Worker thread for video generation to keep UI responsive"""
    progress_update = Signal(int, str)
    finished_success = Signal(Path)
    finished_error = Signal(str)
    
    def __init__(self, audio_file, video_clips, preset_selector):
        super().__init__()
        self.audio_file = audio_file
        self.video_clips = video_clips
        self.preset_selector = preset_selector
        self._is_cancelled = False
    
    def cancel(self):
        self._is_cancelled = True
    
    def run(self):
        try:
            self.progress_update.emit(10, "Loading modules...")
            
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from core.audio_analyzer import AudioAnalyzer
            from core.agi_director_intelligence import AGIDirectorIntelligence
            from core.video_renderer import VideoRenderer
            from core.agi_director_intelligence import ClipAnalysis
            from core.editing_presets import EditingPreset
            from core.agi_director_intelligence import BeatSegment
            from datetime import datetime
            
            if self._is_cancelled:
                return
            
            self.progress_update.emit(20, "Analyzing audio...")
            analyzer = AudioAnalyzer()
            audio_analysis = analyzer.analyze_music(self.audio_file)
            
            if self._is_cancelled:
                return
            
            self.progress_update.emit(30, "Analyzing video clips...")
            analyzed_clips = []
            
            try:
                from services.claude_vision_api import ClaudeVisionAPI
                api = ClaudeVisionAPI()
                
                for i, video_clip in enumerate(self.video_clips):
                    if self._is_cancelled:
                        return
                    
                    self.progress_update.emit(
                        40 + int((i + 1) / len(self.video_clips) * 20),
                        f"Analyzing clip {i+1}/{len(self.video_clips)}..."
                    )
                    
                    clip = api.analyze_clip(
                        video_path=video_clip.filename,
                        duration=float(str(video_clip.duration).replace("s", "")),
                        resolution=(1920, 1080),
                        fps=30.0,
                        codec="h264"
                    )
                    analyzed_clips.append(clip)
            except Exception as e:
                for video_clip in self.video_clips:
                    clip = ClipAnalysis(
                        video_path=video_clip.filename,
                        duration=float(str(video_clip.duration).replace("s", "")),
                        subject_type="person",
                        has_faces=True,
                        face_count=1,
                        art_style="realistic",
                        color_dominant="#FF5733",
                        color_palette=["#FF5733", "#33FF57"],
                        motion_intensity=5.0,
                        composition="medium",
                        energy_level=6.0,
                        mood="energetic",
                        resolution=(1920, 1080),
                        fps=30.0,
                        codec="h264"
                    )
                    analyzed_clips.append(clip)
            
            if self._is_cancelled:
                return
            
            self.progress_update.emit(60, "Getting preferences...")
            
            if hasattr(self.preset_selector, "current_selections"):
                try:
                    editing = self.preset_selector.current_selections["editing"]
                    color = self.preset_selector.current_selections["color"]
                    effects_tuples = self.preset_selector.get_backend_effects()
                    effects = [e[0] for e in effects_tuples] if effects_tuples else ["Clean"]
                except:
                    editing, color, effects = "Balanced", "Natural", "Clean"
            else:
                editing, color, effects = "Balanced", "Natural", "Clean"
            
            self.progress_update.emit(65, "Creating edit plan...")
            
            beats = audio_analysis.get("beats", [])
            beat_segments = []
            for idx in range(len(beats) - 1):
                segment = BeatSegment(
                    start_time=beats[idx],
                    end_time=beats[idx + 1],
                    duration=beats[idx + 1] - beats[idx],
                    beat_index=idx,
                    energy=audio_analysis.get("energy_curve", [0.6])[min(idx, len(audio_analysis.get("energy_curve", [])) - 1)],
                    spectral_flux=0.5,
                    is_drop=False,
                    is_buildup=False,
                    has_vocals=False,
                    tempo=audio_analysis.get("tempo", 120)
                )
                beat_segments.append(segment)
            
            preset_map = {
                "Flash Cuts": "flash_cuts",
                "Balanced": "balanced",
                "Dynamic": "dynamic",
                "Hypercut": "hypercut",
                "EXTREME": "hypercut",
                "Chill": "balanced"
            }
            
            editing_backend = preset_map.get(editing, "balanced")
            preset_data = EditingPreset.get_preset(editing_backend)
            
            preset = {
                "editing": editing_backend,
                "color": color,
                "effects": effects,
                "clip_mix": preset_data.get("clip_mix", {"short": 0.4, "medium": 0.4, "long": 0.2}),
                "duration_range": preset_data.get("duration_range", (2.0, 4.0))
            }
            
            agi = AGIDirectorIntelligence(preset, audio_analysis)
            edit_plan = agi.create_edit_plan(analyzed_clips, beat_segments, audio_analysis.get("duration", 30))
            
            if self._is_cancelled:
                return
            
            self.progress_update.emit(80, "Rendering video...")
            
            output_dir = Path.home() / "Videos" / "BeatSync"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_dir / f"beatsync_{timestamp}.mp4"
            
            renderer = VideoRenderer()
            edit_plan_formatted = {
                "clips": edit_plan,
                "color": color,
                "effects": effects
            }
            
            renderer.render_music_video(edit_plan_formatted, self.audio_file, str(output_path))
            
            if self._is_cancelled:
                return
            
            self.progress_update.emit(100, "Complete!")
            self.finished_success.emit(output_path)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.finished_error.emit(str(e))
