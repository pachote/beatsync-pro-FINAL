"""
BEATSYNC PRO - PREMIUM UI
$100M Professional Design
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

class Colors:
    BG_DEEP = "#0F0F11"
    BG_PANEL = "#18181B"
    BG_ELEVATED = "#1F1F23"
    BG_CARD = "#27272B"
    BG_HOVER = "#2F2F35"
    BLUE_START = "#3B82F6"
    BLUE_END = "#2563EB"
    BLUE_GLOW = "#60A5FA"
    SUCCESS = "#22C55E"
    TEXT_PRIMARY = "#FAFAFA"
    TEXT_SECONDARY = "#D4D4D8"
    TEXT_TERTIARY = "#A1A1AA"
    TEXT_DIM = "#71717A"
    BORDER_SUBTLE = "#27272B"
    BORDER_DEFAULT = "#3F3F46"

class PresetCard(QWidget):
    clicked = Signal()
    
    def __init__(self, icon, title, desc):
        super().__init__()
        self.setFixedHeight(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checked = False
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 28px;")
        layout.addWidget(icon_label)
        
        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        text_layout.addWidget(title_label)
        
        desc_label = QLabel(desc)
        desc_label.setStyleSheet(f"font-size: 11px; color: {Colors.TEXT_TERTIARY};")
        text_layout.addWidget(desc_label)
        
        layout.addLayout(text_layout, 1)
    
    def setChecked(self, checked):
        self._checked = checked
        self.update()
    
    def mousePressEvent(self, event):
        self.clicked.emit()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self._checked:
            painter.setPen(QPen(QColor(Colors.BLUE_START), 2))
            painter.setBrush(QColor(31, 41, 55, 80))
        else:
            painter.setPen(QPen(QColor(Colors.BORDER_DEFAULT), 1))
            painter.setBrush(QColor(Colors.BG_CARD))
        
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 10, 10)

class BeatSyncPremium(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeatSync PRO v15")
        self.setMinimumSize(1600, 900)
        self.presets = []
        self.setup_ui()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main = QVBoxLayout(central)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)
        
        # Top bar
        top = QWidget()
        top.setFixedHeight(64)
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(24, 12, 24, 12)
        
        logo = QLabel("BeatSync PRO")
        logo.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Colors.BLUE_START};")
        top_layout.addWidget(logo)
        top_layout.addStretch()
        
        credits = QLabel("💳 47 Credits")
        credits.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.SUCCESS};")
        top_layout.addWidget(credits)
        
        main.addWidget(top)
        
        # Content area
        content = QHBoxLayout()
        content.setSpacing(1)
        
        # Left panel
        left = QWidget()
        left.setFixedWidth(300)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(20, 20, 20, 20)
        
        audio_btn = QPushButton("🎵 Import Audio")
        audio_btn.setFixedHeight(48)
        left_layout.addWidget(audio_btn)
        
        video_btn = QPushButton("📁 Import Videos")
        video_btn.setFixedHeight(48)
        left_layout.addWidget(video_btn)
        
        left_layout.addStretch()
        content.addWidget(left)
        
        # Center - Video player
        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(20, 20, 20, 20)
        
        video = QVideoWidget()
        video.setMinimumHeight(400)
        center_layout.addWidget(video, 6)
        
        timeline = QLabel("Timeline")
        timeline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timeline.setMinimumHeight(150)
        center_layout.addWidget(timeline, 4)
        
        content.addWidget(center)
        
        # Right panel
        right = QWidget()
        right.setFixedWidth(340)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(16)
        
        header = QLabel("🤖 AI Director")
        header.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Colors.TEXT_PRIMARY};")
        right_layout.addWidget(header)
        
        # Presets
        presets = [
            ("🌊", "Chill", "Smooth, contemplative"),
            ("⚖️", "Balanced", "Mix of pacing"),
            ("⚡", "Dynamic", "Energetic, varied"),
            ("⚡⚡", "Flash Cuts", "Rapid fire"),
            ("🔥", "Hypercut", "Ultra dynamic"),
            ("💥", "EXTREME", "Maximum insanity")
        ]
        
        for icon, title, desc in presets:
            card = PresetCard(icon, title, desc)
            if title == "Balanced":
                card.setChecked(True)
            card.clicked.connect(lambda c=card: self.select_preset(c))
            self.presets.append(card)
            right_layout.addWidget(card)
        
        right_layout.addStretch()
        
        # Generate button
        gen_btn = QPushButton("🎬 Generate Video")
        gen_btn.setFixedHeight(56)
        right_layout.addWidget(gen_btn)
        
        cost = QLabel("Cost: 1 credit")
        cost.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cost.setStyleSheet(f"color: {Colors.SUCCESS}; font-size: 12px;")
        right_layout.addWidget(cost)
        
        content.addWidget(right)
        
        main.addLayout(content)
        
        self.apply_styles()
    
    def select_preset(self, selected):
        for card in self.presets:
            card.setChecked(card == selected)
    
    def apply_styles(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {Colors.BG_DEEP}; }}
            QWidget {{ 
                color: {Colors.TEXT_PRIMARY}; 
                font-family: "Segoe UI", sans-serif;
                font-size: 13px;
            }}
            QPushButton {{
                background-color: {Colors.BG_CARD};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_DEFAULT};
                border-radius: 8px;
                font-weight: 600;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_HOVER};
            }}
            QVideoWidget {{
                background-color: #000;
                border: 1px solid {Colors.BORDER_SUBTLE};
                border-radius: 10px;
            }}
            QLabel {{
                background-color: {Colors.BG_PANEL};
                border: 1px solid {Colors.BORDER_SUBTLE};
                border-radius: 10px;
            }}
        """)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = BeatSyncPremium()
    window.show()
    sys.exit(app.exec())
