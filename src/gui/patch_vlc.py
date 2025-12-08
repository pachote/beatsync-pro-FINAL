with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace play_video_file to use system default player (VLC if installed)
old_play = '''    def play_video_file(self, video_path):
        """Load and play a video file in the preview"""
        from PySide6.QtCore import QUrl
        if not hasattr(self, 'media_player'):
            return
        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        self.media_player.play()
        self.play_btn.setText("⏸")
        print(f"[PLAYER] Playing: {video_path}")'''

new_play = '''    def play_video_file(self, video_path):
        """Load and play a video file - uses system player for smooth playback"""
        import subprocess
        import os
        
        print(f"[PLAYER] Playing: {video_path}")
        
        # Try VLC first (smooth playback), fallback to system default
        vlc_paths = [
            r"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
            r"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
        ]
        
        for vlc_path in vlc_paths:
            if os.path.exists(vlc_path):
                subprocess.Popen([vlc_path, video_path])
                return
        
        # Fallback to system default player
        os.startfile(video_path)'''

if old_play in content:
    content = content.replace(old_play, new_play)
    print("[+] Replaced play_video_file with VLC/system player")
else:
    print("[!] Could not find play_video_file pattern")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[DONE] Video playback now uses VLC or system default!")
