with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix wrong color name
old_style = 'self.audio_scroll.setStyleSheet(f"QScrollArea {{ border: none; background: {ProColors.BG_DARKER}; }} QScrollArea > QWidget > QWidget {{ background: {ProColors.BG_DARKER}; }}")'
new_style = 'self.audio_scroll.setStyleSheet(f"QScrollArea {{ border: none; background: {ProColors.BG_DEEP}; }} QScrollArea > QWidget > QWidget {{ background: {ProColors.BG_DEEP}; }}")'

if old_style in content:
    content = content.replace(old_style, new_style)
    print("[+] Fixed color name to BG_DEEP!")
else:
    print("[!] Could not find style")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)
