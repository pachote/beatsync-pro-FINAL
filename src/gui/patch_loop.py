with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_import_videos = False
skip_until_video_count = False
i = 0

while i < len(lines):
    line = lines[i]
    
    # Detect start of import_videos method
    if "def import_videos(self):" in line:
        in_import_videos = True
        new_lines.append(line)
        i += 1
        continue
    
    # Find "for file_path in files:" and replace the whole loop
    if in_import_videos and "for file_path in files:" in line:
        # Write new loop
        new_lines.append("            for file_path in files:\n")
        new_lines.append("                filename = os.path.basename(file_path)\n")
        new_lines.append("                duration = '8.2s'\n")
        new_lines.append("                resolution = '1920x1080'\n")
        new_lines.append("                \n")
        new_lines.append("                # Check aspect ratio\n")
        new_lines.append("                try:\n")
        new_lines.append("                    import cv2\n")
        new_lines.append("                    cap = cv2.VideoCapture(file_path)\n")
        new_lines.append("                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))\n")
        new_lines.append("                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))\n")
        new_lines.append("                    cap.release()\n")
        new_lines.append("                    resolution = f'{width}x{height}'\n")
        new_lines.append("                    video_aspect = '16:9' if width > height else '9:16'\n")
        new_lines.append("                    \n")
        new_lines.append("                    if self.project_aspect_ratio is None:\n")
        new_lines.append("                        self.project_aspect_ratio = video_aspect\n")
        new_lines.append("                        print(f'[ASPECT] Auto-detected: {self.project_aspect_ratio} ({width}x{height})')\n")
        new_lines.append("                    \n")
        new_lines.append("                    if video_aspect != self.project_aspect_ratio:\n")
        new_lines.append("                        print(f'[ASPECT] REJECTED: {video_aspect} != {self.project_aspect_ratio}')\n")
        new_lines.append("                        rejected_videos.append(filename)\n")
        new_lines.append("                        continue\n")
        new_lines.append("                    print(f'[ASPECT] OK: {video_aspect}')\n")
        new_lines.append("                except Exception as e:\n")
        new_lines.append("                    print(f'[ASPECT] Error: {e}')\n")
        new_lines.append("                \n")
        new_lines.append("                thumb = VideoThumbnail(file_path, duration, resolution)\n")
        new_lines.append("                thumb.toggled.connect(self.on_video_toggled)\n")
        new_lines.append("                thumb.deleted.connect(self.on_video_deleted)\n")
        new_lines.append("                self.video_clips.append(thumb)\n")
        new_lines.append("                self.video_layout.addWidget(thumb)\n")
        new_lines.append("            \n")
        new_lines.append("            # Show warning for rejected videos\n")
        new_lines.append("            if rejected_videos:\n")
        new_lines.append("                self.aspect_warning_label.setText(f'WARNING: {len(rejected_videos)} video(s) rejected - {self.project_aspect_ratio} required')\n")
        new_lines.append("                self.aspect_warning_label.show()\n")
        new_lines.append("            else:\n")
        new_lines.append("                self.aspect_warning_label.hide()\n")
        
        # Skip old loop until we hit video_count_label
        skip_until_video_count = True
        i += 1
        continue
    
    # Skip old loop content
    if skip_until_video_count:
        if "video_count_label.setText" in line:
            skip_until_video_count = False
            in_import_videos = False
            new_lines.append("            \n")
            new_lines.append(line)
        i += 1
        continue
    
    new_lines.append(line)
    i += 1

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("[DONE] import_videos updated with aspect filtering!")
