with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the scroll area styling - make it dark background
old_style = 'self.audio_scroll.setStyleSheet(f"QScrollArea {{ border: none; background: transparent; }}")'
new_style = 'self.audio_scroll.setStyleSheet(f"QScrollArea {{ border: none; background: {ProColors.BG_DARKER}; }} QScrollArea > QWidget > QWidget {{ background: {ProColors.BG_DARKER}; }}")'

if old_style in content:
    content = content.replace(old_style, new_style)
    print("[+] Fixed audio scroll area colors!")
else:
    print("[!] Could not find style to replace")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)
