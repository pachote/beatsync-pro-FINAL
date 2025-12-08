"""
BEATSYNC PRO - PROFESSIONAL UI
Dark theme, single-page layout, preset selector
Based on Adobe Premiere Pro + Topaz Video AI design language
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# COLORS (2025 Futuristic AI Aesthetic)
class Colors:
    BG_MAIN = "#0B0E17"           # Deep space blue-black
    BG_SURFACE = "#1A1D2E"        # Elevated panels
    BG_INPUT = "#252836"          # Form fields
    BG_ELEVATED = "#2D3142"       # Hover states
    
    BLUE_PRIMARY = "#0078D4"      # Microsoft professional blue
    BLUE_HOVER = "#106EBE"        # 10% darker
    BLUE_PRESSED = "#005A9E"      # 20% darker
    BLUE_GLOW = "#4A9EFF"         # Lighter highlights
    BLUE_NEON = "#00F0FF"         # Electric cyan
    
    PURPLE_AI = "#8B5CF6"         # AI processing
    PURPLE_GLOW = "#A855F7"       # Active AI
    
    GREEN_SUCCESS = "#10B981"     # Emerald
    LIME_PROGRESS = "#84CC16"     # Completion
    AMBER_WARNING = "#F59E0B"
    RED_ERROR = "#EF4444"
    
    TEXT_PRIMARY = "#FFFFFF"      # 100% white
    TEXT_SECONDARY = "#B4B8C5"    # 70%
    TEXT_TERTIARY = "#6B7280"     # 60%
    TEXT_DISABLED = "#4B5563"     # 40%
    
    BORDER_REST = "#FFFFFF1F"     # 12% white
    BORDER_HOVER = "#FFFFFF33"    # 20% white
    DIVIDER = "#404040"

class BeatSyncProUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeatSync PRO - AI Music Video Director")
        self.setMinimumSize(1920, 1080)
        
        # Apply dark theme
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {Colors.BG_MAIN};
            }}
            QWidget {{
                color: {Colors.TEXT_PRIMARY};
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 14px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
            }}
            QPushButton {{
                background-color: {Colors.BG_INPUT};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_REST};
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_ELEVATED};
                border-color: {Colors.BORDER_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BLUE_PRESSED};
            }}
            QRadioButton {{
                color: {Colors.TEXT_PRIMARY};
                spacing: 8px;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid {Colors.BORDER_REST};
                background-color: {Colors.BG_INPUT};
            }}
            QRadioButton::indicator:checked {{
                background-color: {Colors.BLUE_PRIMARY};
                border-color: {Colors.BLUE_PRIMARY};
            }}
        """)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI layout"""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # TOP BAR (80px)
        main_layout.addWidget(self.create_top_bar())
        
        # MIDDLE SECTION (Left + Center + Right)
        middle = QHBoxLayout()
        middle.setSpacing(0)
        middle.addWidget(self.create_left_panel())
        middle.addWidget(self.create_center_panel())
        middle.addWidget(self.create_right_panel())
        main_layout.addLayout(middle)
        
        # BOTTOM BAR (60px)
        main_layout.addWidget(self.create_bottom_bar())
    
    def create_top_bar(self):
        """Audio import section"""
        bar = QWidget()
        bar.setFixedHeight(80)
        bar.setStyleSheet(f"background-color: {Colors.BG_SURFACE};")
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(24, 16, 24, 16)
        
        # Audio drop zone
        drop_zone = QLabel("🎵 Drag audio file here or click to browse\nMP3, WAV, FLAC • Max 6 minutes")
        drop_zone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_zone.setStyleSheet(f"""
            background-color: {Colors.BG_INPUT};
            border: 2px dashed {Colors.BORDER_HOVER};
            border-radius: 8px;
            padding: 16px;
            color: {Colors.TEXT_SECONDARY};
        """)
        layout.addWidget(drop_zone)
        
        return bar
    
    def create_left_panel(self):
        """Video library - 300px"""
        panel = QWidget()
        panel.setFixedWidth(300)
        panel.setStyleSheet(f"background-color: {Colors.BG_SURFACE};")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header
        header = QLabel("Video Library (0/300 clips)")
        header.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(header)
        
        # Import button
        import_btn = QPushButton("+ Import Videos")
        import_btn.setFixedHeight(40)
        layout.addWidget(import_btn)
        
        # Clip grid (placeholder)
        clips_area = QLabel("No clips imported\n\nDrag videos here or click Import")
        clips_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clips_area.setStyleSheet(f"""
            background-color: {Colors.BG_INPUT};
            border-radius: 8px;
            padding: 48px;
            color: {Colors.TEXT_TERTIARY};
        """)
        layout.addWidget(clips_area, 1)
        
        return panel
    
    def create_center_panel(self):
        """Preview + Timeline"""
        panel = QWidget()
        panel.setStyleSheet(f"background-color: {Colors.BG_MAIN};")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Video preview (60%)
        preview = QLabel("Video Preview\n\n▶ No video loaded")
        preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview.setStyleSheet(f"""
            background-color: #000000;
            border: 1px solid {Colors.DIVIDER};
            border-radius: 8px;
            color: {Colors.TEXT_TERTIARY};
            font-size: 16px;
        """)
        layout.addWidget(preview, 60)
        
        # Timeline (40%)
        timeline = QLabel("Timeline\n\nWaveform + Beat Markers")
        timeline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timeline.setStyleSheet(f"""
            background-color: {Colors.BG_SURFACE};
            border: 1px solid {Colors.DIVIDER};
            border-radius: 8px;
            color: {Colors.TEXT_TERTIARY};
        """)
        layout.addWidget(timeline, 40)
        
        return panel
    
    def create_right_panel(self):
        """AI Controls - 340px"""
        panel = QWidget()
        panel.setFixedWidth(340)
        panel.setStyleSheet(f"background-color: {Colors.BG_SURFACE};")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        
        # PRESET SELECTOR
        presets_label = QLabel("Editing Style")
        presets_label.setStyleSheet(f"font-size: 16px; font-weight: 600;")
        layout.addWidget(presets_label)
        
        presets = [
            ("Chill", "30-40 clips, 3-5 sec each\nSlow, smooth. Ballads, acoustic."),
            ("Balanced", "50-70 clips, 2-4 sec each\nMix of pacing. Most genres."),
            ("Dynamic", "80-100 clips, 1.5-3 sec each\nFast-paced. Pop and rock."),
            ("Flash Cuts", "120-150 clips, 0.5-1.5 sec\nRapid cuts. Electronic."),
            ("Hypercut", "180-250 clips, 0.3-1 sec\nExtreme cutting. Experimental."),
        ]
        
        self.preset_group = QButtonGroup()
        for i, (name, desc) in enumerate(presets):
            preset_widget = self.create_preset_card(name, desc, i == 1)  # Balanced default
            layout.addWidget(preset_widget)
        
        layout.addStretch()
        
        # GENERATE BUTTON
        generate_btn = QPushButton("🎬 Generate Video")
        generate_btn.setFixedHeight(56)
        generate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BLUE_PRIMARY};
                color: {Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: {Colors.BLUE_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BLUE_PRESSED};
            }}
        """)
        layout.addWidget(generate_btn)
        
        return panel
    
    def create_preset_card(self, name, description, checked=False):
        """Create a preset selection card"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.BG_INPUT};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        
        radio = QRadioButton(name)
        radio.setChecked(checked)
        radio.setStyleSheet(f"font-weight: 600; font-size: 15px;")
        self.preset_group.addButton(radio)
        layout.addWidget(radio)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 12px; margin-left: 28px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return card
    
    def create_bottom_bar(self):
        """Export settings"""
        bar = QWidget()
        bar.setFixedHeight(60)
        bar.setStyleSheet(f"background-color: {Colors.BG_SURFACE}; border-top: 1px solid {Colors.DIVIDER};")
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(24, 12, 24, 12)
        
        layout.addWidget(QLabel("Quality:"))
        quality_combo = QComboBox()
        quality_combo.addItems(["720p", "1080p", "4K"])
        quality_combo.setCurrentIndex(1)
        layout.addWidget(quality_combo)
        
        layout.addWidget(QLabel("Format:"))
        format_combo = QComboBox()
        format_combo.addItems(["MP4", "MOV", "WebM"])
        layout.addWidget(format_combo)
        
        layout.addStretch()
        
        export_btn = QPushButton("📤 Export")
        export_btn.setFixedHeight(40)
        layout.addWidget(export_btn)
        
        return bar

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    # Set Inter font if available
    font = QFont("Inter", 10)
    app.setFont(font)
    
    window = BeatSyncProUI()
    window.show()
    sys.exit(app.exec())
