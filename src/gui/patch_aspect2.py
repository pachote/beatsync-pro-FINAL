# Read file
with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the import_videos method and rewrite the loop
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Find "rejected_videos = []" and rewrite from there
    if "rejected_videos = []" in line:
        new_lines.append("            rejected_videos = []\n")
        new_lines.append("            \n")
        i += 1
        
        # Skip to "for file_path in files:"
        while i < len(lines) and "for file_path in files:" not in lines[i]:
            i += 1
        
        # Add the new loop
        new_lines.append("            for file_path in files:\n")
        new_lines.append("                filename = os.path.basename(file_path)\n")
        new_lines.append("                duration = \"8.2s\"\n")
        new_lines.append("                resolution = \"1920x1080\"\n")
        new_lines.append("                \n")
        new_lines.append("                # Get actual video dimensions and check aspect ratio\n")
        new_lines.append("                try:\n")
        new_lines.append("                    import cv2\n")
        new_lines.append("                    cap = cv2.VideoCapture(file_path)\n")
        new_lines.append("                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))\n")
        new_lines.append("                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))\n")
        new_lines.append("                    cap.release()\n")
        new_lines.append("                    resolution = f\"{width}x{height}\"\n")
        new_lines.append("                    \n")
        new_lines.append("                    # Determine this video's aspect ratio\n")
        new_lines.append("                    if width > height:\n")
        new_lines.append("                        video_aspect = '16:9'\n")
        new_lines.append("                    else:\n")
        new_lines.append("                        video_aspect = '9:16'\n")
        new_lines.append("                    \n")
        new_lines.append("                    # Auto-detect project aspect from first video\n")
        new_lines.append("                    if self.project_aspect_ratio is None:\n")
        new_lines.append("                        self.project_aspect_ratio = video_aspect\n")
        new_lines.append("                        print(f'[ASPECT] Auto-detected: {self.project_aspect_ratio} ({width}x{height})')\n")
        new_lines.append("                    \n")
        new_lines.append("                    # Check if matches project aspect ratio\n")
        new_lines.append("                    if video_aspect != self.project_aspect_ratio:\n")
        new_lines.append("                        print(f'[ASPECT] REJECTED: {video_aspect} != {self.project_aspect_ratio}')\n")
        new_lines.append("                        rejected_videos.append({'filename': filename, 'aspect': video_aspect, 'resolution': resolution})\n")
        new_lines.append("                        continue  # Skip this video\n")
        new_lines.append("                    else:\n")
        new_lines.append("                        print(f'[ASPECT] Validated: {video_aspect} matches')\n")
        new_lines.append("                except Exception as e:\n")
        new_lines.append("                    print(f'[ASPECT] Could not detect: {e}')\n")
        new_lines.append("                \n")
        new_lines.append("                thumb = VideoThumbnail(file_path, duration, resolution)\n")
        new_lines.append("                thumb.toggled.connect(self.on_video_toggled)\n")
        new_lines.append("                thumb.deleted.connect(self.on_video_deleted)\n")
        new_lines.append("                self.video_clips.append(thumb)\n")
        new_lines.append("                self.video_layout.addWidget(thumb)\n")
        new_lines.append("            \n")
        new_lines.append("            # Show warning for rejected videos\n")
        new_lines.append("            if rejected_videos:\n")
        new_lines.append("                rejected_list = chr(10).join([f'- {v[\"filename\"]} ({v[\"aspect\"]})' for v in rejected_videos])\n")
        new_lines.append("                msg = f\"{len(rejected_videos)} video(s) rejected (wrong aspect ratio).\\n\\nProject: {self.project_aspect_ratio}\\n\\nRejected:\\n{rejected_list}\"\n")
        new_lines.append("                self.show_styled_warning(\"Aspect Ratio Mismatch\", msg)\n")
        new_lines.append("            \n")
        i += 1
        
        # Skip the old loop content until we hit video_count_label
        while i < len(lines) and "video_count_label.setText" not in lines[i]:
            i += 1
        # Don't increment - we want to keep this line
        continue
    else:
        new_lines.append(line)
    i += 1

# Write file
with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("[DONE] import_videos fully rewritten with aspect ratio filtering!")
