with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Replace play_video_file method
    if "def play_video_file(self, video_path):" in line:
        new_lines.append("    def play_video_file(self, video_path):\n")
        new_lines.append('        """Play video using embedded VLC player"""\n')
        new_lines.append('        import sys\n')
        new_lines.append('        print(f"[PLAYER] Playing: {video_path}")\n')
        new_lines.append('        \n')
        new_lines.append('        # Set VLC to render in our widget (Windows)\n')
        new_lines.append('        if sys.platform == "win32":\n')
        new_lines.append('            self.vlc_player.set_hwnd(int(self.video_widget.winId()))\n')
        new_lines.append('        \n')
        new_lines.append('        # Load and play media\n')
        new_lines.append('        media = self.vlc_instance.media_new(video_path)\n')
        new_lines.append('        self.vlc_player.set_media(media)\n')
        new_lines.append('        self.vlc_player.play()\n')
        new_lines.append('        self.play_btn.setText("⏸")\n')
        new_lines.append('    \n')
        
        # Skip old method
        i += 1
        while i < len(lines) and not lines[i].strip().startswith("def "):
            i += 1
        print("[+] Replaced play_video_file with VLC version")
        continue
    
    # Replace toggle_playback method  
    if "def toggle_playback(self):" in line:
        new_lines.append("    def toggle_playback(self):\n")
        new_lines.append('        """Toggle VLC playback"""\n')
        new_lines.append('        if not hasattr(self, "vlc_player"):\n')
        new_lines.append('            return\n')
        new_lines.append('        \n')
        new_lines.append('        if self.vlc_player.is_playing():\n')
        new_lines.append('            self.vlc_player.pause()\n')
        new_lines.append('            self.play_btn.setText("▶")\n')
        new_lines.append('        else:\n')
        new_lines.append('            self.vlc_player.play()\n')
        new_lines.append('            self.play_btn.setText("⏸")\n')
        new_lines.append('    \n')
        
        # Skip old method
        i += 1
        while i < len(lines) and not lines[i].strip().startswith("def "):
            i += 1
        print("[+] Replaced toggle_playback with VLC version")
        continue
    
    new_lines.append(line)
    i += 1

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("[DONE] VLC playback methods updated!")
