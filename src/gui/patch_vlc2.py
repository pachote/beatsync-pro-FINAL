with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip_until_next_def = False
i = 0

while i < len(lines):
    line = lines[i]
    
    # Find play_video_file method
    if "def play_video_file(self, video_path):" in line:
        # Write new implementation
        new_lines.append("    def play_video_file(self, video_path):\n")
        new_lines.append('        """Launch video in VLC or system player for smooth playback"""\n')
        new_lines.append("        import subprocess\n")
        new_lines.append("        import os\n")
        new_lines.append("        \n")
        new_lines.append('        print(f"[PLAYER] Launching: {video_path}")\n')
        new_lines.append("        \n")
        new_lines.append("        # Try VLC first for smooth playback\n")
        new_lines.append("        vlc_paths = [\n")
        new_lines.append('            r"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",\n')
        new_lines.append('            r"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"\n')
        new_lines.append("        ]\n")
        new_lines.append("        \n")
        new_lines.append("        for vlc_path in vlc_paths:\n")
        new_lines.append("            if os.path.exists(vlc_path):\n")
        new_lines.append("                subprocess.Popen([vlc_path, video_path])\n")
        new_lines.append("                return\n")
        new_lines.append("        \n")
        new_lines.append("        # Fallback to system default\n")
        new_lines.append("        os.startfile(video_path)\n")
        new_lines.append("    \n")
        
        # Skip old method until next def or class
        skip_until_next_def = True
        i += 1
        print(f"[+] Found play_video_file at line {i}")
        continue
    
    if skip_until_next_def:
        # Check if we hit next method definition
        if line.strip().startswith("def ") and "play_video_file" not in line:
            skip_until_next_def = False
            new_lines.append(line)
        i += 1
        continue
    
    new_lines.append(line)
    i += 1

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("[DONE] play_video_file now uses VLC!")
