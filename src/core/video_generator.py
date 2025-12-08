import os
from src.core.claude_director import ClaudeDirector
import subprocess
from src.core.claude_director import ClaudeDirector
from pathlib import Path
from src.core.claude_director import ClaudeDirector
from PySide6.QtCore import QThread, Signal
import json

from src.core.claude_director import ClaudeDirector
class VideoGeneratorWorker(QThread):
    progress = Signal(int, str)
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, edit_plan, music_path, output_path):
        super().__init__()
        self.edit_plan = edit_plan
        self.music_path = music_path
        self.output_path = output_path
    
    def run(self):
        try:
            self.progress.emit(10, 'Creating clip list...')
            
            clips = self.edit_plan.get('clips', [])
            if not clips:
                self.error.emit('No clips in edit plan!')
                return
            
            self.progress.emit(20, f'Processing {len(clips)} clips...')
            
            # Create temp directory
            temp_dir = Path('temp_render')
            temp_dir.mkdir(exist_ok=True)
            
            # Create FFmpeg concat file
            concat_file = temp_dir / 'concat.txt'
            print(f'\n?? DEBUG: Processing {len(clips)} clips for concat')
            with open(concat_file, 'w') as f:
                for i, clip in enumerate(clips):
                    video_path = clip.get('video_path', '')
                    print(f'  Clip {i}: path="{video_path}", exists={os.path.exists(video_path)}')
                    if os.path.exists(video_path):
                        # Escape single quotes in path
                        escaped_path = video_path.replace("'", "'\\\\''")
                        f.write(f"file '{escaped_path}'\n")
                        duration = clip.get('clip_duration', 3)
                        f.write(f"duration {duration}\n")
            
            self.progress.emit(40, 'Concatenating clips...')
            
            # Concatenate videos
            temp_video = temp_dir / 'temp_video.mp4'
            concat_cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                str(temp_video)
            ]
            
            subprocess.run(concat_cmd, check=True, capture_output=True)
            
            self.progress.emit(60, 'Adding music...')
            
            # Add music
            final_cmd = [
                'ffmpeg', '-y',
                '-i', str(temp_video),
                '-i', self.music_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',
                self.output_path
            ]
            
            subprocess.run(final_cmd, check=True, capture_output=True)
            
            self.progress.emit(100, 'Complete!')
            self.finished.emit(self.output_path)
            
        except subprocess.CalledProcessError as e:
            self.error.emit(f'FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}')
        except Exception as e:
            self.error.emit(f'Error: {str(e)}')

