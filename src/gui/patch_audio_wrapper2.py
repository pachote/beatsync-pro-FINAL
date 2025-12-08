with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# Simple targeted replacement - find the line that adds audio_container directly
old_line = "        layout.addWidget(self.audio_container)"

# Check what comes before to make sure we're in the right spot
if "self.audio_layout.addWidget(self.audio_empty)" in content and old_line in content:
    
    # Replace the audio_container section with wrapped version
    old_block = """        self.audio_container = QWidget()

        self.audio_layout = QVBoxLayout(self.audio_container)

        self.audio_layout.setContentsMargins(0, 0, 0, 0)

        self.audio_layout.setSpacing(8)

        
        self.audio_empty = QLabel("No audio tracks imported")

        self.audio_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.audio_empty.setStyleSheet(f"color: {ProColors.TEXT_DIM}; font-size: 11px; padding: 20px 0;")

        self.audio_layout.addWidget(self.audio_empty)

        
        layout.addWidget(self.audio_container)"""

    new_block = """        # FIXED: Wrap audio container in fixed-height frame to prevent expansion
        audio_wrapper = QFrame()
        audio_wrapper.setFixedHeight(120)  # Lock height - prevents panel expansion!
        wrapper_layout = QVBoxLayout(audio_wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)
        
        # Scroll area inside the fixed wrapper
        self.audio_scroll = QScrollArea()
        self.audio_scroll.setWidgetResizable(True)
        self.audio_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.audio_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.audio_scroll.setStyleSheet(f"QScrollArea {{ border: none; background: transparent; }}")
        
        self.audio_container = QWidget()
        self.audio_layout = QVBoxLayout(self.audio_container)
        self.audio_layout.setContentsMargins(0, 0, 0, 0)
        self.audio_layout.setSpacing(8)
        self.audio_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.audio_empty = QLabel("No audio tracks imported")
        self.audio_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_empty.setStyleSheet(f"color: {ProColors.TEXT_DIM}; font-size: 11px; padding: 20px 0;")
        self.audio_layout.addWidget(self.audio_empty)

        self.audio_scroll.setWidget(self.audio_container)
        wrapper_layout.addWidget(self.audio_scroll)
        layout.addWidget(audio_wrapper)"""

    if old_block in content:
        content = content.replace(old_block, new_block)
        print("[+] APPLIED FIX with exact block match!")
    else:
        # Try line by line replacement
        lines = content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            if 'self.audio_container = QWidget()' in lines[i] and i > 2000 and i < 2100:
                # Found the target area - skip old lines and insert new block
                print(f"[+] Found audio_container at line {i+1}")
                # Skip until we find layout.addWidget(self.audio_container)
                while i < len(lines) and 'layout.addWidget(self.audio_container)' not in lines[i]:
                    i += 1
                i += 1  # Skip the addWidget line too
                # Insert new block
                new_lines.append("        # FIXED: Wrap audio container in fixed-height frame to prevent expansion")
                new_lines.append("        audio_wrapper = QFrame()")
                new_lines.append("        audio_wrapper.setFixedHeight(120)  # Lock height - prevents panel expansion!")
                new_lines.append("        wrapper_layout = QVBoxLayout(audio_wrapper)")
                new_lines.append("        wrapper_layout.setContentsMargins(0, 0, 0, 0)")
                new_lines.append("        wrapper_layout.setSpacing(0)")
                new_lines.append("        ")
                new_lines.append("        # Scroll area inside the fixed wrapper")
                new_lines.append("        self.audio_scroll = QScrollArea()")
                new_lines.append("        self.audio_scroll.setWidgetResizable(True)")
                new_lines.append("        self.audio_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)")
                new_lines.append("        self.audio_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)")
                new_lines.append('        self.audio_scroll.setStyleSheet(f"QScrollArea {{ border: none; background: transparent; }}")')
                new_lines.append("        ")
                new_lines.append("        self.audio_container = QWidget()")
                new_lines.append("        self.audio_layout = QVBoxLayout(self.audio_container)")
                new_lines.append("        self.audio_layout.setContentsMargins(0, 0, 0, 0)")
                new_lines.append("        self.audio_layout.setSpacing(8)")
                new_lines.append("        self.audio_layout.setAlignment(Qt.AlignmentFlag.AlignTop)")
                new_lines.append("        ")
                new_lines.append('        self.audio_empty = QLabel("No audio tracks imported")')
                new_lines.append("        self.audio_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)")
                new_lines.append('        self.audio_empty.setStyleSheet(f"color: {ProColors.TEXT_DIM}; font-size: 11px; padding: 20px 0;")')
                new_lines.append("        self.audio_layout.addWidget(self.audio_empty)")
                new_lines.append("        ")
                new_lines.append("        self.audio_scroll.setWidget(self.audio_container)")
                new_lines.append("        wrapper_layout.addWidget(self.audio_scroll)")
                new_lines.append("        layout.addWidget(audio_wrapper)")
                print("[+] APPLIED FIX via line-by-line replacement!")
            else:
                new_lines.append(lines[i])
                i += 1
        content = '\n'.join(new_lines)
else:
    print("[!] Could not find target code section")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[DONE]")
