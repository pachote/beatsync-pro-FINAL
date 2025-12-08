"""
BEATSYNC PRO - TOPAZ-STYLE PROFESSIONAL UI
Premium design matching Topaz Video AI quality
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

class TopazColors:
    # Topaz-inspired professional palette
    BG_DEEP = "#1C1C1E"          # Deep charcoal
    BG_SURFACE = "#2C2C2E"       # Surface
    BG_ELEVATED = "#363639"      # Elevated
    BG_INPUT = "#3A3A3C"         # Inputs
    
    PURPLE_PRIMARY = "#8B5CF6"   # Vibrant purple (Topaz style)
    PURPLE_HOVER = "#9D6EF7"
    PURPLE_DARK = "#7C3AED"
    PURPLE_GLOW = "#A78BFA"
    
    BLUE_ACCENT = "#3B82F6"
    GREEN_SUCCESS = "#10B981"
    
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#E5E5E7"
    TEXT_TERTIARY = "#AEAEB2"
    TEXT_DIM = "#8E8E93"
    
    BORDER = "#48484A"
    DIVIDER = "#38383A"

class ToggleSwitch(QWidget):
    """Professional toggle switch like Topaz"""
    toggled = Signal(bool)
    
    def __init__(self, checked=False):
        super().__init__()
        self.setFixedSize(44, 24)
        self._checked = checked
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def isChecked(self):
        return self._checked
    
    def setChecked(self, checked):
        self._checked = checked
        self.update()
    
    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.toggled.emit(self._checked)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Track
        if self._checked:
            painter.setBrush(QColor(TopazColors.PURPLE_PRIMARY))
        else:
            painter.setBrush(QColor(TopazColors.BG_INPUT))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 44, 24, 12, 12)
        
        # Thumb
        thumb_x = 22 if self._checked else 2
        painter.setBrush(QColor(TopazColors.TEXT_PRIMARY))
        painter.drawEllipse(thumb_x, 2, 20, 20)

class PresetCard(QWidget):
    """Clean preset card - Topaz style"""
    clicked = Signal()
    
    def __init__(self, icon, title, subtitle):
        super().__init__()
        self.setFixedHeight(72)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checked = False
        self._hovered = False
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(14)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 26px; color: {TopazColors.PURPLE_PRIMARY};")
        icon_label.setFixedWidth(32)
        layout.addWidget(icon_label)
        
        # Text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {TopazColors.TEXT_PRIMARY};
        """)
        text_layout.addWidget(title_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(f"""
            font-size: 11px;
            color: {TopazColors.TEXT_TERTIARY};
        """)
        text_layout.addWidget(subtitle_label)
        
        layout.addLayout(text_layout, 1)
    
    def setChecked(self, checked):
        self._checked = checked
        self.update()
    
    def enterEvent(self, event):
        self._hovered = True
        self.update()
    
    def leaveEvent(self, event):
        self._hovered = False
        self.update()
    
    def mousePressEvent(self, event):
        self.clicked.emit()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        if self._checked:
            # Selected - purple border
            painter.setPen(QPen(QColor(TopazColors.PURPLE_PRIMARY), 2))
            painter.setBrush(QColor(123, 58, 237, 25))  # Purple tint
        elif self._hovered:
            painter.setPen(QPen(QColor(TopazColors.BORDER), 1))
            painter.setBrush(QColor(TopazColors.BG_ELEVATED))
        else:
            painter.setPen(QPen(QColor(TopazColors.BORDER), 1))
            painter.setBrush(QColor(TopazColors.BG_SURFACE))
        
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 8, 8)

class BeatSyncTopaz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeatSync PRO v15")
        self.setMinimumSize(1680, 960)
        self.resize(1920, 1080)
        self.presets = []
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        # Menu bar
        self.create_menu()
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main = QVBoxLayout(central)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)
        
        # Top bar
        main.addWidget(self.create_top_bar())
        
        # Main content
        content = QHBoxLayout()
        content.setSpacing(0)
        content.addWidget(self.create_left_panel())
        content.addWidget(self.create_center_panel())
        content.addWidget(self.create_right_panel())
        main.addLayout(content, 1)
        
        # Bottom timeline
        main.addWidget(self.create_bottom_panel())
    
    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Import Audio...", None, "Ctrl+I")
        file_menu.addAction("Import Videos...", None, "Ctrl+Shift+I")
        
        edit_menu = menubar.addMenu("Edit")
        view_menu = menubar.addMenu("View")
        process_menu = menubar.addMenu("Process")
        account_menu = menubar.addMenu("Account")
        help_menu = menubar.addMenu("Help")
    
    def create_top_bar(self):
        bar = QWidget()
        bar.setFixedHeight(56)
        bar.setObjectName("topBar")
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 8, 20, 8)
        
        # Logo
        logo = QLabel("🎵 BeatSync PRO")
        logo.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 700;
            color: {TopazColors.TEXT_PRIMARY};
        """)
        layout.addWidget(logo)
        
        layout.addStretch()
        
        # Credits badge
        credits_badge = QWidget()
        credits_badge.setObjectName("creditsBadge")
        cred_layout = QHBoxLayout(credits_badge)
        cred_layout.setContentsMargins(12, 6, 12, 6)
        cred_layout.setSpacing(8)
        
        cred_icon = QLabel("💳")
        cred_layout.addWidget(cred_icon)
        
        cred_label = QLabel("47 Credits")
        cred_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {TopazColors.GREEN_SUCCESS};")
        cred_layout.addWidget(cred_label)
        
        layout.addWidget(credits_badge)
        
        # Account button
        account_btn = QPushButton("Demo User")
        account_btn.setObjectName("accountBtn")
        account_btn.setFixedHeight(36)
        layout.addWidget(account_btn)
        
        return bar
    
    def create_left_panel(self):
        panel = QWidget()
        panel.setFixedWidth(260)
        panel.setObjectName("leftPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(16)
        
        # Audio section
        audio_label = QLabel("AUDIO TRACK")
        audio_label.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 700;
            color: {TopazColors.TEXT_TERTIARY};
            letter-spacing: 1px;
        """)
        layout.addWidget(audio_label)
        
        audio_btn = QPushButton("🎵 Import Audio")
        audio_btn.setObjectName("importBtn")
        audio_btn.setFixedHeight(44)
        layout.addWidget(audio_btn)
        
        audio_info = QLabel("No audio\nMax 6 minutes")
        audio_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        audio_info.setStyleSheet(f"color: {TopazColors.TEXT_DIM}; font-size: 11px; padding: 12px;")
        layout.addWidget(audio_info)
        
        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"background: {TopazColors.DIVIDER}; max-height: 1px;")
        layout.addWidget(line)
        
        # Video section
        video_label = QLabel("VIDEO CLIPS")
        video_label.setStyleSheet(audio_label.styleSheet())
        layout.addWidget(video_label)
        
        video_btn = QPushButton("📁 Import Videos")
        video_btn.setObjectName("importBtn")
        video_btn.setFixedHeight(44)
        layout.addWidget(video_btn)
        
        clips_info = QLabel("0/300 clips\nMax 15s each")
        clips_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clips_info.setStyleSheet(audio_info.styleSheet())
        layout.addWidget(clips_info)
        
        layout.addStretch()
        
        return panel
    
    def create_center_panel(self):
        panel = QWidget()
        panel.setObjectName("centerPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Video preview
        video = QVideoWidget()
        video.setMinimumHeight(480)
        video.setObjectName("videoPreview")
        layout.addWidget(video, 7)
        
        # Playback controls
        controls = self.create_player_controls()
        layout.addWidget(controls)
        
        # Timeline preview
        timeline = QLabel("Timeline • Waveform • Beat Markers")
        timeline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timeline.setMinimumHeight(120)
        timeline.setObjectName("timelinePreview")
        timeline.setStyleSheet(f"""
            background: {TopazColors.BG_SURFACE};
            border: 1px solid {TopazColors.BORDER};
            border-radius: 8px;
            color: {TopazColors.TEXT_DIM};
            font-size: 12px;
        """)
        layout.addWidget(timeline, 3)
        
        return panel
    
    def create_player_controls(self):
        controls = QWidget()
        controls.setFixedHeight(56)
        controls.setObjectName("playerControls")
        
        layout = QHBoxLayout(controls)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Play button
        play = QPushButton("▶")
        play.setFixedSize(40, 40)
        play.setObjectName("playBtn")
        layout.addWidget(play)
        
        # Timeline slider
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setObjectName("timeSlider")
        layout.addWidget(slider, 1)
        
        # Time
        time_label = QLabel("0:00 / 0:00")
        time_label.setStyleSheet(f"color: {TopazColors.TEXT_SECONDARY}; font-family: monospace; font-size: 12px;")
        layout.addWidget(time_label)
        
        return controls
    
    def create_right_panel(self):
        panel = QWidget()
        panel.setFixedWidth(340)
        panel.setObjectName("rightPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # AI Director header
        header = QLabel("🤖 AI Director")
        header.setStyleSheet(f"""
            font-size: 17px;
            font-weight: 700;
            color: {TopazColors.TEXT_PRIMARY};
        """)
        layout.addWidget(header)
        
        # Editing Intensity
        intensity_label = QLabel("EDITING INTENSITY")
        intensity_label.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 700;
            color: {TopazColors.TEXT_TERTIARY};
            letter-spacing: 1px;
            margin-top: 8px;
        """)
        layout.addWidget(intensity_label)
        
        # Presets
        presets = [
            ("🌊", "Chill", "Smooth, contemplative"),
            ("⚖️", "Balanced", "Mix of pacing"),
            ("⚡", "Dynamic", "Energetic, varied"),
            ("⚡⚡", "Flash Cuts", "Rapid fire"),
            ("🔥", "Hypercut", "Ultra dynamic"),
            ("💥", "EXTREME", "Maximum intensity")
        ]
        
        for icon, title, subtitle in presets:
            card = PresetCard(icon, title, subtitle)
            if title == "Balanced":
                card.setChecked(True)
            card.clicked.connect(lambda c=card: self.select_preset(c))
            self.presets.append(card)
            layout.addWidget(card)
        
        layout.addStretch()
        
        # Settings section
        settings_label = QLabel("GENERATION SETTINGS")
        settings_label.setStyleSheet(intensity_label.styleSheet())
        layout.addWidget(settings_label)
        
        # Quality
        q_row = self.create_setting_row("Quality:", ["720p", "1080p", "4K"], 1)
        layout.addLayout(q_row)
        
        # Lip Sync
        lip_row = self.create_setting_row("Lip Sync:", ["None", "Sync Labs", "Rask AI"], 0)
        layout.addLayout(lip_row)
        
        # Generate button
        gen_btn = QPushButton("🎬 Generate Video")
        gen_btn.setFixedHeight(52)
        gen_btn.setObjectName("generateBtn")
        layout.addWidget(gen_btn)
        
        # Cost
        cost = QLabel("Cost: 1 credit")
        cost.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cost.setStyleSheet(f"color: {TopazColors.GREEN_SUCCESS}; font-size: 12px; font-weight: 600;")
        layout.addWidget(cost)
        
        return panel
    
    def create_setting_row(self, label_text, options, default_idx):
        row = QHBoxLayout()
        row.setSpacing(12)
        
        label = QLabel(label_text)
        label.setStyleSheet(f"color: {TopazColors.TEXT_TERTIARY}; font-size: 12px;")
        label.setFixedWidth(70)
        row.addWidget(label)
        
        combo = QComboBox()
        combo.addItems(options)
        combo.setCurrentIndex(default_idx)
        combo.setFixedHeight(36)
        combo.setObjectName("settingCombo")
        row.addWidget(combo, 1)
        
        return row
    
    def create_bottom_panel(self):
        panel = QWidget()
        panel.setFixedHeight(140)
        panel.setObjectName("bottomPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Header
        header = QLabel("CLIP LIBRARY")
        header.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 700;
            color: {TopazColors.TEXT_TERTIARY};
            letter-spacing: 1px;
        """)
        layout.addWidget(header)
        
        # Thumbnail area
        thumbs = QLabel("Video thumbnails will appear here")
        thumbs.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumbs.setStyleSheet(f"""
            background: {TopazColors.BG_SURFACE};
            border: 1px solid {TopazColors.BORDER};
            border-radius: 6px;
            color: {TopazColors.TEXT_DIM};
            font-size: 12px;
            padding: 20px;
        """)
        layout.addWidget(thumbs, 1)
        
        return panel
    
    def select_preset(self, selected):
        for card in self.presets:
            card.setChecked(card == selected)
    
    def apply_theme(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background: {TopazColors.BG_DEEP};
            }}
            QWidget {{
                color: {TopazColors.TEXT_PRIMARY};
                font-family: -apple-system, "Segoe UI", sans-serif;
                font-size: 13px;
            }}
            QMenuBar {{
                background: {TopazColors.BG_SURFACE};
                border-bottom: 1px solid {TopazColors.BORDER};
                padding: 6px 8px;
                font-size: 13px;
            }}
            QMenuBar::item {{
                padding: 6px 12px;
                border-radius: 5px;
            }}
            QMenuBar::item:selected {{
                background: {TopazColors.BG_ELEVATED};
            }}
            #topBar {{
                background: {TopazColors.BG_SURFACE};
                border-bottom: 1px solid {TopazColors.BORDER};
            }}
            #creditsBadge {{
                background: {TopazColors.BG_ELEVATED};
                border: 1px solid {TopazColors.BORDER};
                border-radius: 8px;
            }}
            #accountBtn {{
                background: {TopazColors.BG_ELEVATED};
                border: 1px solid {TopazColors.BORDER};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
            }}
            #accountBtn:hover {{
                background: {TopazColors.BG_INPUT};
            }}
            #leftPanel, #rightPanel {{
                background: {TopazColors.BG_SURFACE};
                border-right: 1px solid {TopazColors.BORDER};
            }}
            #centerPanel {{
                background: {TopazColors.BG_DEEP};
            }}
            #videoPreview {{
                background: #000;
                border: 1px solid {TopazColors.BORDER};
                border-radius: 8px;
            }}
            #playerControls {{
                background: {TopazColors.BG_SURFACE};
                border: 1px solid {TopazColors.BORDER};
                border-radius: 8px;
            }}
            #playBtn {{
                background: {TopazColors.PURPLE_PRIMARY};
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }}
            #playBtn:hover {{
                background: {TopazColors.PURPLE_HOVER};
            }}
            #timeSlider::groove:horizontal {{
                height: 4px;
                background: {TopazColors.BG_INPUT};
                border-radius: 2px;
            }}
            #timeSlider::handle:horizontal {{
                width: 12px;
                height: 12px;
                background: {TopazColors.PURPLE_PRIMARY};
                border-radius: 6px;
                margin: -4px 0;
            }}
            #timeSlider::sub-page:horizontal {{
                background: {TopazColors.PURPLE_PRIMARY};
                border-radius: 2px;
            }}
            #importBtn {{
                background: {TopazColors.BG_ELEVATED};
                border: 1px solid {TopazColors.BORDER};
                border-radius: 8px;
                font-weight: 600;
                padding: 10px;
            }}
            #importBtn:hover {{
                background: {TopazColors.BG_INPUT};
                border-color: {TopazColors.PURPLE_PRIMARY};
            }}
            #generateBtn {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {TopazColors.PURPLE_PRIMARY},
                    stop:1 {TopazColors.PURPLE_DARK});
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 0.3px;
            }}
            #generateBtn:hover {{
                background: {TopazColors.PURPLE_HOVER};
            }}
            #settingCombo {{
                background: {TopazColors.BG_INPUT};
                border: 1px solid {TopazColors.BORDER};
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 500;
            }}
            #settingCombo:hover {{
                border-color: {TopazColors.PURPLE_PRIMARY};
            }}
            #settingCombo::drop-down {{
                border: none;
                padding-right: 8px;
            }}
            #bottomPanel {{
                background: {TopazColors.BG_SURFACE};
                border-top: 1px solid {TopazColors.BORDER};
            }}
        """)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = BeatSyncTopaz()
    window.show()
    sys.exit(app.exec())
