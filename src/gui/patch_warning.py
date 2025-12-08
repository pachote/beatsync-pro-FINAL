# Simple patch - add warning label and aspect ratio filtering
with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add warning label after video_count_label creation (around line 2073)
old_count_label = '''self.video_count_label.setStyleSheet(f"font-size: 10px; color: {ProColors.TEXT_DIM};")
        video_header_layout.addStretch()
        video_header_layout.addWidget(self.video_count_label)'''

new_count_label = '''self.video_count_label.setStyleSheet(f"font-size: 10px; color: {ProColors.TEXT_DIM};")
        video_header_layout.addStretch()
        video_header_layout.addWidget(self.video_count_label)
        
        # Aspect ratio warning label
        self.aspect_warning_label = QLabel("")
        self.aspect_warning_label.setStyleSheet("font-size: 11px; color: #ff6b6b; font-weight: bold; padding: 4px;")
        self.aspect_warning_label.setWordWrap(True)
        self.aspect_warning_label.hide()'''

if old_count_label in content:
    content = content.replace(old_count_label, new_count_label)
    print("[+] Added aspect_warning_label to UI")
else:
    print("[!] Could not find video_count_label pattern")

# 2. Add warning label to layout after video_btn
old_btn = '''video_btn.clicked.connect(self.import_videos)
        layout.addWidget(video_btn)
        # Multi-select controls'''

new_btn = '''video_btn.clicked.connect(self.import_videos)
        layout.addWidget(video_btn)
        layout.addWidget(self.aspect_warning_label)
        # Multi-select controls'''

if old_btn in content:
    content = content.replace(old_btn, new_btn)
    print("[+] Added warning label to layout")
else:
    print("[!] Could not find video_btn pattern")

# 3. Replace import_videos loop with aspect filtering
old_loop = '''if files:
            # video_empty removed
            rejected_videos = []
            for file_path in files:
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

new_loop = '''if files:
            rejected_videos = []
            for file_path in files:
                filename = os.path.basename(file_path)
                duration = "8.2s"
                resolution = "1920x1080"
                
                # Check aspect ratio
                try:
                    import cv2
                    cap = cv2.VideoCapture(file_path)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cap.release()
                    resolution = f"{width}x{height}"
                    video_aspect = '16:9' if width > height else '9:16'
                    
                    # Set project aspect from first video
                    if self.project_aspect_ratio is None:
                        self.project_aspect_ratio = video_aspect
                        print(f'[ASPECT] Auto-detected: {self.project_aspect_ratio} ({width}x{height})')
                    
                    # Reject mismatched aspect ratios
                    if video_aspect != self.project_aspect_ratio:
                        print(f'[ASPECT] REJECTED: {video_aspect} != {self.project_aspect_ratio}')
                        rejected_videos.append(filename)
                        continue
                    print(f'[ASPECT] OK: {video_aspect}')
                except Exception as e:
                    print(f'[ASPECT] Error: {e}')
                
                thumb = VideoThumbnail(file_path, duration, resolution)
                thumb.toggled.connect(self.on_video_toggled)
                thumb.deleted.connect(self.on_video_deleted)
                self.video_clips.append(thumb)
                self.video_layout.addWidget(thumb)
            
            # Show/hide warning
            if rejected_videos:
                self.aspect_warning_label.setText(f"⚠ {len(rejected_videos)} video(s) rejected - wrong aspect ratio ({self.project_aspect_ratio} required)")
                self.aspect_warning_label.show()
            else:
                self.aspect_warning_label.hide()'''

if old_loop in content:
    content = content.replace(old_loop, new_loop)
    print("[+] Updated import_videos with aspect filtering")
else:
    print("[!] Could not find import loop - trying alternate")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\n[DONE] Patch complete!")
