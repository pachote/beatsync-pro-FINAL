with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip_next_duplicates = False
found_first_setVideoOutput = False

for i, line in enumerate(lines):
    # Track when we've seen the first setVideoOutput
    if "self.media_player.setVideoOutput(video)" in line:
        if not found_first_setVideoOutput:
            found_first_setVideoOutput = True
            new_lines.append(line)
        else:
            # Skip this duplicate and the next two lines (positionChanged, durationChanged)
            skip_next_duplicates = 2
            print(f"[+] Skipping duplicate setVideoOutput at line {i+1}")
            continue
    elif skip_next_duplicates > 0:
        skip_next_duplicates -= 1
        print(f"[+] Skipping duplicate signal at line {i+1}")
        continue
    else:
        new_lines.append(line)

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("[DONE] Removed duplicate player setup!")
