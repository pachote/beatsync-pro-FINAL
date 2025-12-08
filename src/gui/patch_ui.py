import re

with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    
    # After video_count_label added to layout, add warning label
    if "video_header_layout.addWidget(self.video_count_label)" in line:
        new_lines.append("\n")
        new_lines.append("        # Aspect ratio warning label\n")
        new_lines.append("        self.aspect_warning_label = QLabel('')\n")
        new_lines.append("        self.aspect_warning_label.setStyleSheet('font-size: 11px; color: #ff6b6b; font-weight: bold;')\n")
        new_lines.append("        self.aspect_warning_label.hide()\n")
        print(f"[+] Added warning label definition at line {i+1}")
    
    # After video_btn added to layout, add warning label to layout
    if "layout.addWidget(video_btn)" in line and "video_btn" in line:
        new_lines.append("        layout.addWidget(self.aspect_warning_label)\n")
        print(f"[+] Added warning label to layout at line {i+1}")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("[DONE] Warning label added to UI!")
