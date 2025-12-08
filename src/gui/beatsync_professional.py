"""
BEATSYNC PRO - PROFESSIONAL UI
$100M Quality - Topaz Video AI Standard
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

class ProColors:
    # Professional blue color scheme (like Topaz)
    BG_DEEP = "#1A1D23"          # Deep dark blue-gray
    BG_SURFACE = "#252932"       # Surface panels
    BG_ELEVATED = "#2D3139"      # Elevated elements
    BG_INPUT = "#353B45"         # Input fields
    
    BLUE_PRIMARY = "#4A9EFF"     # Bright professional blue
    BLUE_HOVER = "#5BAEFF"
    BLUE_DARK = "#3B8EEF"
    BLUE_GLOW = "#6FB6FF"
    
    GREEN_SUCCESS = "#0ECB81"
    AMBER_WARNING = "#F6B93B"
    RED_ERROR = "#E84855"
    
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#C5CBD3"
    TEXT_TERTIARY = "#8F95A3"
    TEXT_DIM = "#6B7280"
    
    BORDER = "#3A404A"
    DIVIDER = "#2F3541"

class ToggleSwitch(QWidget):
    """Professional toggle - Topaz style"""
    toggled = Signal(bool)
    
    def __init__(self, checked=False):
        super().__init__()
        self.setFixedSize(44, 24)
        self._checked = checked
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._animation = QPropertyAnimation(self, b"thumbPosition")
        self._animation.setDuration(150)
        self._thumb_pos = 22 if checked else 2
    
    def thumbPosition(self):
        return self._thumb_pos
    
    def setThumbPosition(self, pos):
        self._thumb_pos = pos
        self.update()
    
    thumbPosition = Property(int, thumbPosition, setThumbPosition)
    
    def isChecked(self):
        return self._checked
    
    def setChecked(self, checked):
        self._checked = checked
        self._animation.setStartValue(self._thumb_pos)
        self._animation.setEndValue(22 if checked else 2)
        self._animation.start()
    
    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.setChecked(self._checked)
        self.toggled.emit(self._checked)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Track
        if self._checked:
            painter.setBrush(QColor(ProColors.BLUE_PRIMARY))
        else:
            painter.setBrush(QColor(ProColors.BG_INPUT))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 44, 24, 12, 12)
        
        # Thumb
        painter.setBrush(QColor(ProColors.TEXT_PRIMARY))
        painter.drawEllipse(int(self._thumb_pos), 2, 20, 20)

class PresetCard(QWidget):
    """Professional preset card"""
    clicked = Signal()
    
    def __init__(self, title, subtitle):
        super().__init__()
        self.setFixedHeight(68)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checked = False
        self._hovered = False
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {ProColors.TEXT_PRIMARY};
            background: transparent;
            border: none;
        """)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(f"""
            font-size: 11px;
            color: {ProColors.TEXT_TERTIARY};
            background: transparent;
            border: none;
        """)
        layout.addWidget(subtitle_label)
    
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
            painter.setPen(QPen(QColor(ProColors.BLUE_PRIMARY), 2))
            painter.setBrush(QColor(74, 158, 255, 15))  # Blue tint
        elif self._hovered:
            painter.setPen(QPen(QColor(ProColors.BORDER), 1))
            painter.setBrush(QColor(ProColors.BG_ELEVATED))
        else:
            painter.setPen(QPen(QColor(ProColors.BORDER), 1))
            painter.setBrush(QColor(ProColors.BG_SURFACE))
        
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 6, 6)

class BeatSyncProfessional(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeatSync PRO v15")
        self.setMinimumSize(1680, 960)
        self.resize(1920, 1080)
        self.presets = []
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        self.create_menu()
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main = QVBoxLayout(central)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)
        
        main.addWidget(self.create_top_bar())
        
        content = QHBoxLayout()
        content.setSpacing(0)
        content.addWidget(self.create_left_panel())
        content.addWidget(self.create_center_panel())
        content.addWidget(self.create_right_panel())
        main.addLayout(content, 1)
        
        main.addWidget(self.create_bottom_panel())
    
    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Import Audio...", None, "Ctrl+I")
        file_menu.addAction("Import Videos...", None, "Ctrl+Shift+I")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close, "Ctrl+Q")
        
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Process")
        menubar.addMenu("Account")
        menubar.addMenu("Help")
    
    def create_top_bar(self):
        bar = QWidget()
        bar.setFixedHeight(52)
        bar.setObjectName("topBar")
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 8, 20, 8)
        
        logo = QLabel("BeatSync PRO")
        logo.setStyleSheet(f"""
            font-size: 15px;
            font-weight: 700;
            color: {ProColors.TEXT_PRIMARY};
            letter-spacing: 0.5px;
        """)
        layout.addWidget(logo)
        
        version = QLabel("v15")
        version.setStyleSheet(f"font-size: 11px; color: {ProColors.TEXT_DIM}; margin-left: 8px;")
        layout.addWidget(version)
        
        layout.addStretch()
        
        # Credits
        credits_widget = QWidget()
        credits_widget.setObjectName("creditsBadge")
        cred_layout = QHBoxLayout(credits_widget)
        cred_layout.setContentsMargins(10, 5, 10, 5)
        cred_layout.setSpacing(6)
        
        cred_label = QLabel("47 Credits")
        cred_label.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {ProColors.GREEN_SUCCESS};")
        cred_layout.addWidget(cred_label)
        
        layout.addWidget(credits_widget)
        
        # Account
        account_btn = QPushButton("Demo User")
        account_btn.setObjectName("accountBtn")
        account_btn.setFixedHeight(32)
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
            font-size: 10px;
            font-weight: 700;
            color: {ProColors.TEXT_TERTIARY};
            letter-spacing: 1.2px;
        """)
        layout.addWidget(audio_label)
        
        audio_btn = QPushButton("Import Audio")
        audio_btn.setObjectName("importBtn")
        audio_btn.setFixedHeight(40)
        layout.addWidget(audio_btn)
        
        audio_info = QLabel("No audio loaded\nMax 6 minutes")
        audio_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        audio_info.setStyleSheet(f"color: {ProColors.TEXT_DIM}; font-size: 11px; padding: 10px;")
        layout.addWidget(audio_info)
        
        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"background: {ProColors.DIVIDER}; max-height: 1px; margin: 8px 0;")
        layout.addWidget(line)
        
        # Video section
        video_label = QLabel("VIDEO CLIPS")
        video_label.setStyleSheet(audio_label.styleSheet())
        layout.addWidget(video_label)
        
        video_btn = QPushButton("Import Videos")
        video_btn.setObjectName("importBtn")
        video_btn.setFixedHeight(40)
        layout.addWidget(video_btn)
        
        clips_info = QLabel("0/300 clips loaded\nMax 15 seconds each")
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
        layout.setSpacing(10)
        
        # Video preview
        video = QVideoWidget()
        video.setMinimumHeight(480)
        video.setObjectName("videoPreview")
        layout.addWidget(video, 7)
        
        # Controls
        controls = self.create_controls()
        layout.addWidget(controls)
        
        # Timeline
        timeline = QLabel("Timeline • Waveform • Beat Markers")
        timeline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timeline.setMinimumHeight(120)
        timeline.setObjectName("timelinePreview")
        layout.addWidget(timeline, 3)
        
        return panel
    
    def create_controls(self):
        controls = QWidget()
        controls.setFixedHeight(52)
        controls.setObjectName("playerControls")
        
        layout = QHBoxLayout(controls)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # Play
        play = QPushButton("▶")
        play.setFixedSize(36, 36)
        play.setObjectName("playBtn")
        layout.addWidget(play)
        
        # Slider
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setObjectName("timeSlider")
        layout.addWidget(slider, 1)
        
        # Time
        time_label = QLabel("0:00 / 0:00")
        time_label.setStyleSheet(f"""
            color: {ProColors.TEXT_SECONDARY};
            font-family: 'Consolas', monospace;
            font-size: 11px;
            font-weight: 500;
        """)
        layout.addWidget(time_label)
        
        return controls
    
    def create_right_panel(self):
        panel = QWidget()
        panel.setFixedWidth(340)
        panel.setObjectName("rightPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)
        
        # Header
        header = QLabel("AI Director")
        header.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 700;
            color: {ProColors.TEXT_PRIMARY};
        """)
        layout.addWidget(header)
        
        # Editing Intensity
        intensity_label = QLabel("EDITING INTENSITY")
        intensity_label.setStyleSheet(f"""
            font-size: 10px;
            font-weight: 700;
            color: {ProColors.TEXT_TERTIARY};
            letter-spacing: 1.2px;
            margin-top: 4px;
        """)
        layout.addWidget(intensity_label)
        
        # Presets
        presets = [
            ("Chill", "Smooth, contemplative pacing"),
            ("Balanced", "Mix of pacing • Recommended"),
            ("Dynamic", "Energetic, varied cuts"),
            ("Flash Cuts", "Rapid fire editing"),
            ("Hypercut", "Ultra dynamic cuts"),
            ("EXTREME", "Maximum intensity")
        ]
        
        for title, subtitle in presets:
            card = PresetCard(title, subtitle)
            if title == "Balanced":
                card.setChecked(True)
            card.clicked.connect(lambda c=card: self.select_preset(c))
            self.presets.append(card)
            layout.addWidget(card)
        
        layout.addStretch()
        
        # Settings
        settings_label = QLabel("GENERATION SETTINGS")
        settings_label.setStyleSheet(intensity_label.styleSheet())
        layout.addWidget(settings_label)
        
        # Quality
        q_row = QHBoxLayout()
        q_label = QLabel("Quality")
        q_label.setStyleSheet(f"color: {ProColors.TEXT_TERTIARY}; font-size: 12px;")
        q_label.setFixedWidth(70)
        q_row.addWidget(q_label)
        
        q_combo = QComboBox()
        q_combo.addItems(["720p", "1080p", "4K"])
        q_combo.setCurrentIndex(1)
        q_combo.setFixedHeight(34)
        q_combo.setObjectName("settingCombo")
        q_row.addWidget(q_combo, 1)
        
        layout.addLayout(q_row)
        
        # Lip Sync
        lip_row = QHBoxLayout()
        lip_label = QLabel("Lip Sync")
        lip_label.setStyleSheet(q_label.styleSheet())
        lip_label.setFixedWidth(70)
        lip_row.addWidget(lip_label)
        
        lip_combo = QComboBox()
        lip_combo.addItems(["None", "Sync Labs", "Rask AI"])
        lip_combo.setFixedHeight(34)
        lip_combo.setObjectName("settingCombo")
        lip_row.addWidget(lip_combo, 1)
        
        layout.addLayout(lip_row)
        
        # Generate button
        gen_btn = QPushButton("Generate Video")
        gen_btn.setFixedHeight(48)
        gen_btn.setObjectName("generateBtn")
        layout.addWidget(gen_btn)
        
        # Cost
        cost = QLabel("Cost: 1 credit")
        cost.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cost.setStyleSheet(f"color: {ProColors.GREEN_SUCCESS}; font-size: 11px; font-weight: 600;")
        layout.addWidget(cost)
        
        return panel
    
    def create_bottom_panel(self):
        panel = QWidget()
        panel.setFixedHeight(140)
        panel.setObjectName("bottomPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 12, 16, 12)
        
        header = QLabel("CLIP LIBRARY")
        header.setStyleSheet(f"""
            font-size: 10px;
            font-weight: 700;
            color: {ProColors.TEXT_TERTIARY};
            letter-spacing: 1.2px;
        """)
        layout.addWidget(header)
        
        thumbs = QLabel("Video clip thumbnails will appear here")
        thumbs.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumbs.setStyleSheet(f"""
            background: {ProColors.BG_SURFACE};
            border: 1px solid {ProColors.BORDER};
            border-radius: 6px;
            color: {ProColors.TEXT_DIM};
            font-size: 11px;
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
                background: {ProColors.BG_DEEP};
            }}
            QWidget {{
                color: {ProColors.TEXT_PRIMARY};
                font-family: -apple-system, "Segoe UI", sans-serif;
                font-size: 13px;
            }}
            QMenuBar {{
                background: {ProColors.BG_SURFACE};
                border-bottom: 1px solid {ProColors.BORDER};
                padding: 5px 8px;
                font-size: 13px;
            }}
            QMenuBar::item {{
                padding: 5px 12px;
                border-radius: 4px;
            }}
            QMenuBar::item:selected {{
                background: {ProColors.BG_ELEVATED};
            }}
            #topBar {{
                background: {ProColors.BG_SURFACE};
                border-bottom: 1px solid {ProColors.BORDER};
            }}
            #creditsBadge {{
                background: {ProColors.BG_ELEVATED};
                border: 1px solid {ProColors.BORDER};
                border-radius: 6px;
            }}
            #accountBtn {{
                background: {ProColors.BG_ELEVATED};
                border: 1px solid {ProColors.BORDER};
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: 500;
            }}
            #accountBtn:hover {{
                background: {ProColors.BG_INPUT};
                border-color: {ProColors.BLUE_PRIMARY};
            }}
            #leftPanel, #rightPanel {{
                background: {ProColors.BG_SURFACE};
            }}
            #leftPanel {{
                border-right: 1px solid {ProColors.BORDER};
            }}
            #rightPanel {{
                border-left: 1px solid {ProColors.BORDER};
            }}
            #centerPanel {{
                background: {ProColors.BG_DEEP};
            }}
            #videoPreview {{
                background: #000000;
                border: 1px solid {ProColors.BORDER};
                border-radius: 6px;
            }}
            #playerControls {{
                background: {ProColors.BG_SURFACE};
                border: 1px solid {ProColors.BORDER};
                border-radius: 6px;
            }}
            #playBtn {{
                background: {ProColors.BLUE_PRIMARY};
                color: white;
                border: none;
                border-radius: 18px;
                font-size: 12px;
                font-weight: bold;
            }}
            #playBtn:hover {{
                background: {ProColors.BLUE_HOVER};
            }}
            #timeSlider::groove:horizontal {{
                height: 4px;
                background: {ProColors.BG_INPUT};
                border-radius: 2px;
            }}
            #timeSlider::handle:horizontal {{
                width: 12px;
                height: 12px;
                background: {ProColors.BLUE_PRIMARY};
                border-radius: 6px;
                margin: -4px 0;
            }}
            #timeSlider::sub-page:horizontal {{
                background: {ProColors.BLUE_PRIMARY};
                border-radius: 2px;
            }}
            #importBtn {{
                background: {ProColors.BG_ELEVATED};
                border: 1px solid {ProColors.BORDER};
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
                padding: 8px;
            }}
            #importBtn:hover {{
                background: {ProColors.BG_INPUT};
                border-color: {ProColors.BLUE_PRIMARY};
            }}
            #generateBtn {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ProColors.BLUE_PRIMARY},
                    stop:1 {ProColors.BLUE_DARK});
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.3px;
            }}
            #generateBtn:hover {{
                background: {ProColors.BLUE_HOVER};
            }}
            #generateBtn:pressed {{
                background: {ProColors.BLUE_DARK};
            }}
            #settingCombo {{
                background: {ProColors.BG_INPUT};
                border: 1px solid {ProColors.BORDER};
                border-radius: 5px;
                padding: 7px 10px;
                font-size: 12px;
                font-weight: 500;
            }}
            #settingCombo:hover {{
                border-color: {ProColors.BLUE_PRIMARY};
            }}
            #settingCombo::drop-down {{
                border: none;
                padding-right: 8px;
            }}
            #timelinePreview {{
                background: {ProColors.BG_SURFACE};
                border: 1px solid {ProColors.BORDER};
                border-radius: 6px;
                color: {ProColors.TEXT_DIM};
                font-size: 11px;
            }}
            #bottomPanel {{
                background: {ProColors.BG_SURFACE};
                border-top: 1px solid {ProColors.BORDER};
            }}
        """)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = BeatSyncProfessional()
    window.show()
    sys.exit(app.exec())
