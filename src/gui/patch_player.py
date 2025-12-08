with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix duplicate setVideoOutput and signal connections
old_player = '''        self.media_player.setVideoOutput(video)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.playbackStateChanged.connect(self.on_playback_state_changed)
        self.media_player.setVideoOutput(video)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)'''

new_player = '''        self.media_player.setVideoOutput(video)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.playbackStateChanged.connect(self.on_playback_state_changed)
        
        # Optimize for smoother playback
        self.media_player.setPlaybackRate(1.0)'''

if old_player in content:
    content = content.replace(old_player, new_player)
    print("[+] Fixed duplicate player setup and optimized")
else:
    print("[!] Pattern not found - checking for duplicates...")
    # Try to find and remove just the duplicates
    dup = '''        self.media_player.setVideoOutput(video)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        layout.addWidget(video, 7)'''
    
    fixed = '''        # Playback rate set for smooth video
        self.media_player.setPlaybackRate(1.0)
        layout.addWidget(video, 7)'''
    
    if dup in content:
        content = content.replace(dup, fixed)
        print("[+] Removed duplicates")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[DONE]")
