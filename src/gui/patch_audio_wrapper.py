with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# THE DEFINITIVE FIX: Wrap audio_container in a fixed-height QFrame
old_code = '''        self.audio_container = QWidget()

        self.audio_layout = QVBoxLayout(self.audio_container)

        self.audio_layout.setContentsMargins(0, 0, 0, 0)

        self.audio_layout.setSpacing(8)



        self.audio_empty = QLabel("No audio tracks imported")

        self.audio_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.audio_empty.setStyleSheet(f"color: {ProColors.TEXT_DIM}; font-size: 11px; padding: 20px 0;")

        self.audio_layout.addWidget(self.audio_empty)



        layout.addWidget(self.audio_container)'''

new_code = '''        # FIXED: Wrap audio container in fixed-height frame to prevent expansion
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
        layout.addWidget(audio_wrapper)'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("[+] APPLIED DEFINITIVE FIX: Audio container wrapped in fixed-height QFrame!")
else:
    print("[!] Could not find exact pattern")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)
