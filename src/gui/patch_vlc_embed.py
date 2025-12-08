with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
i = 0
vlc_import_added = False

while i < len(lines):
    line = lines[i]
    
    # Add VLC import after PySide6 multimedia imports
    if "from PySide6.QtMultimediaWidgets import QVideoWidget" in line and not vlc_import_added:
        new_lines.append(line)
        new_lines.append("\n")
        new_lines.append("# VLC for smooth video playback\n")
        new_lines.append("import vlc\n")
        vlc_import_added = True
        print("[+] Added VLC import")
        i += 1
        continue
    
    # Replace QVideoWidget setup with VLC widget
    if "video = QVideoWidget()" in line:
        new_lines.append("        # VLC player for smooth playback\n")
        new_lines.append("        self.vlc_instance = vlc.Instance('--no-xlib')\n")
        new_lines.append("        self.vlc_player = self.vlc_instance.media_player_new()\n")
        new_lines.append("        \n")
        new_lines.append("        # Create frame to embed VLC\n")
        new_lines.append("        from PySide6.QtWidgets import QFrame\n")
        new_lines.append("        video = QFrame()\n")
        print("[+] Replaced QVideoWidget with VLC frame")
        i += 1
        continue
    
    # Skip QMediaPlayer setup lines
    if "self.media_player = QMediaPlayer()" in line:
        # Skip the old media player setup
        while i < len(lines) and "layout.addWidget(video" not in lines[i]:
            i += 1
        new_lines.append("        # Store video frame reference\n")
        new_lines.append("        self.video_widget = video\n")
        new_lines.append("        self.vlc_widget_id = None  # Will be set when widget is shown\n")
        new_lines.append("        \n")
        print("[+] Replaced QMediaPlayer with VLC player reference")
        continue
    
    new_lines.append(line)
    i += 1

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("[DONE] VLC widget setup added!")
