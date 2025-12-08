import re

# Read file
with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add show_styled_warning method after __init__ in BeatSyncUltimate class
# Find the line after "self.setup_ui()" in BeatSyncUltimate.__init__
init_pattern = r'(        self\.setup_ui\(\)\n)'
warning_method = '''        self.setup_ui()

    def show_styled_warning(self, title, message):
        """Show styled warning popup"""
        from PySide6.QtWidgets import QMessageBox
        msgbox = QMessageBox(self)
        msgbox.setWindowTitle(title)
        msgbox.setText(message)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setStyleSheet(
            'QMessageBox { background-color: #1e1e1e; color: #ffffff; } '
            'QMessageBox QLabel { color: #ffffff; font-size: 13px; padding: 10px; } '
            'QPushButton { background-color: #3a86ff; color: white; border: none; '
            'border-radius: 4px; padding: 8px 20px; font-weight: bold; min-width: 80px; } '
            'QPushButton:hover { background-color: #5094ff; } '
            'QPushButton:pressed { background-color: #2875ef; }'
        )
        msgbox.exec()

'''

# Only add if not already present
if 'def show_styled_warning' not in content:
    content = content.replace('        self.setup_ui()\n', warning_method, 1)
    print("[+] Added show_styled_warning method")
else:
    print("[=] show_styled_warning already exists")

# 2. Replace the import_videos loop to add aspect ratio filtering
# Find the for loop that processes files
old_loop = '''            for file_path in files:

                filename = os.path.basename(file_path)

                duration = "8.2s"

                resolution = "1920x1080"



                thumb = VideoThumbnail(file_path, duration, resolution)

                thumb.toggled.connect(self.on_video_toggled)

                thumb.deleted.connect(self.on_video_deleted)



                self.video_clips.append(thumb)

                self.video_layout.addWidget(thumb)



                # Auto-detect aspect ratio from first video

                if len(self.video_clips) == 1:

                    try:

                        import cv2

                        cap = cv2.VideoCapture(file_path)

                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                        cap.release()

                        if width > height:

                            self.project_aspect_ratio = '16:9'

                        else:

                            self.project_aspect_ratio = '9:16'

                        print(f'[ASPECT] Auto-detected: {self.project_aspect_ratio} ({width}x{height})')

                    except Exception as e:

                        print(f'[ASPECT] Could not detect: {e}')'''

new_loop = '''            rejected_videos = []
            
            for file_path in files:
                filename = os.path.basename(file_path)
                duration = "8.2s"
                resolution = "1920x1080"
                
                # Get actual video dimensions
                try:
                    import cv2
                    cap = cv2.VideoCapture(file_path)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cap.release()
                    resolution = f"{width}x{height}"
                    
                    # Determine this video's aspect ratio
                    if width > height:
                        video_aspect = '16:9'
                    else:
                        video_aspect = '9:16'
                    
                    # Auto-detect project aspect from first video
                    if self.project_aspect_ratio is None:
                        self.project_aspect_ratio = video_aspect
                        print(f'[ASPECT] Auto-detected: {self.project_aspect_ratio} ({width}x{height})')
                    
                    # Check if matches project aspect ratio
                    if video_aspect != self.project_aspect_ratio:
                        print(f'[ASPECT] REJECTED: {video_aspect} != {self.project_aspect_ratio}')
                        rejected_videos.append({
                            'filename': filename,
                            'aspect': video_aspect,
                            'resolution': resolution
                        })
                        continue  # Skip this video
                    else:
                        print(f'[ASPECT] Validated: {video_aspect} matches')
                        
                except Exception as e:
                    print(f'[ASPECT] Could not detect: {e}')
                
                thumb = VideoThumbnail(file_path, duration, resolution)
                thumb.toggled.connect(self.on_video_toggled)
                thumb.deleted.connect(self.on_video_deleted)
                
                self.video_clips.append(thumb)
                self.video_layout.addWidget(thumb)
            
            # Show warning for rejected videos
            if rejected_videos:
                rejected_list = "\\n".join([f"- {v['filename']} ({v['aspect']})" for v in rejected_videos])
                msg = f"{len(rejected_videos)} video(s) rejected due to aspect ratio mismatch.\\n\\nProject: {self.project_aspect_ratio}\\n\\nRejected:\\n{rejected_list}"
                self.show_styled_warning("Aspect Ratio Mismatch", msg)'''

if old_loop in content:
    content = content.replace(old_loop, new_loop)
    print("[+] Updated import_videos with aspect ratio filtering")
else:
    print("[!] Could not find exact loop pattern - checking for simpler pattern")
    # Try simpler replacement
    if 'rejected_videos = []' not in content:
        # Find where we can insert
        simple_old = '            for file_path in files:\n\n                filename = os.path.basename(file_path)'
        simple_new = '            rejected_videos = []\n            \n            for file_path in files:\n                filename = os.path.basename(file_path)'
        if simple_old in content:
            content = content.replace(simple_old, simple_new)
            print("[+] Added rejected_videos list")

# Write file
with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\n[DONE] Patch complete!")
