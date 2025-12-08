"""
BEATSYNC PRO - COMPLETE UI WITH VIDEO PLAYER
Real-time preview + full playback controls
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
import os

class VideoPlayerWidget(QWidget):
    """Professional video player with real-time preview"""
    
    def __init__(self):
        super().__init__()
        self.is_generating = False
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Video display area
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(400)
        self.video_widget.setStyleSheet("""
            QVideoWidget {
                background-color: #000000;
                border: 1px solid #3D3D3D;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.video_widget)
        
        # Status overlay (shown during generation)
        self.status_widget = self.create_status_overlay()
        layout.addWidget(self.status_widget)
        self.status_widget.hide()
        
        # Player controls
        controls = self.create_player_controls()
        layout.addWidget(controls)
        
        # Media player
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)
    
    def create_status_overlay(self):
        """Real-time generation status"""
        widget = QWidget()
        widget.setObjectName("statusOverlay")
        widget.setStyleSheet("""
            #statusOverlay {
                background-color: rgba(0, 0, 0, 0.85);
                border-radius: 8px;
                padding: 24px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.status_title = QLabel("🎬 Generating Video...")
        self.status_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1E90FF;")
        self.status_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_title)
        
        self.status_label = QLabel("Initializing AI Director...")
        self.status_label.setStyleSheet("font-size: 14px; color: #E0E0E0; margin-top: 8px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2D2D2D;
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #1E90FF;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        self.fps_label = QLabel("⚡ Processing at 0 FPS")
        self.fps_label.setStyleSheet("font-size: 12px; color: #9E9E9E; margin-top: 12px;")
        self.fps_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.fps_label)
        
        return widget
    
    def create_player_controls(self):
        """Playback controls"""
        controls = QWidget()
        controls.setFixedHeight(60)
        controls.setObjectName("playerControls")
        
        layout = QHBoxLayout(controls)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Play/Pause button
        self.play_btn = QPushButton("▶")
        self.play_btn.setFixedSize(40, 40)
        self.play_btn.setObjectName("playButton")
        self.play_btn.clicked.connect(self.toggle_play)
        layout.addWidget(self.play_btn)
        
        # Previous frame
        prev_btn = QPushButton("⏮")
        prev_btn.setFixedSize(32, 32)
        layout.addWidget(prev_btn)
        
        # Timeline slider
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setObjectName("timelineSlider")
        layout.addWidget(self.timeline_slider, 1)
        
        # Next frame
        next_btn = QPushButton("⏭")
        next_btn.setFixedSize(32, 32)
        layout.addWidget(next_btn)
        
        # Time display
        self.time_label = QLabel("0:00 / 0:00")
        self.time_label.setStyleSheet("color: #E0E0E0; font-family: monospace; font-size: 13px;")
        self.time_label.setFixedWidth(100)
        layout.addWidget(self.time_label)
        
        # Volume
        volume_btn = QPushButton("🔊")
        volume_btn.setFixedSize(32, 32)
        layout.addWidget(volume_btn)
        
        return controls
    
    def toggle_play(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.play_btn.setText("▶")
        else:
            self.media_player.play()
            self.play_btn.setText("⏸")
    
    def start_generation(self, total_clips):
        """Show generation overlay"""
        self.is_generating = True
        self.status_widget.show()
        self.progress_bar.setMaximum(total_clips)
        self.progress_bar.setValue(0)
    
    def update_generation(self, current_clip, total_clips, fps):
        """Update generation progress"""
        self.progress_bar.setValue(current_clip)
        percent = int((current_clip / total_clips) * 100)
        self.status_label.setText(f"Clip {current_clip}/{total_clips} • {percent}% Complete")
        self.fps_label.setText(f"⚡ Processing at {fps} FPS")
    
    def finish_generation(self, video_path):
        """Load finished video"""
        self.is_generating = False
        self.status_widget.hide()
        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        self.play_btn.setText("▶")

class CreditCalculator:
    """Real-time credit calculation"""
    
    @staticmethod
    def calculate(num_clips, audio_duration_sec, lip_sync_model=None):
        # Base costs
        vision_cost = (num_clips / 100) * 0.80
        director_cost = 0.15
        base = vision_cost + director_cost
        
        # Lip sync
        if lip_sync_model == "sync_labs":
            lipsync = audio_duration_sec * 0.05
        elif lip_sync_model == "rask_ai":
            lipsync = (audio_duration_sec / 60) * 1.50
        else:
            lipsync = 0
        
        total = base + lipsync
        return max(1, round(total))

class EditingPresets:
    """Intensity-based presets"""
    
    PRESETS = {
        'chill': {'name': 'Chill', 'intensity': 0.2, 'description': 'Smooth, contemplative\nLets clips breathe', 'icon': '🌊'},
        'balanced': {'name': 'Balanced', 'intensity': 0.5, 'description': 'Mix of pacing\nMost versatile', 'icon': '⚖️'},
        'dynamic': {'name': 'Dynamic', 'intensity': 0.7, 'description': 'Energetic, varied\nResponds to beats', 'icon': '⚡'},
        'flash_cuts': {'name': 'Flash Cuts', 'intensity': 0.85, 'description': 'Rapid fire\nQuick + holds', 'icon': '⚡⚡'},
        'hypercut': {'name': 'Hypercut', 'intensity': 0.95, 'description': 'Ultra dynamic\nStrategic chaos', 'icon': '🔥'},
        'extreme': {'name': 'EXTREME', 'intensity': 1.0, 'description': 'Maximum insanity\nEvery beat', 'icon': '💥'}
    }

class BeatSyncProMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeatSync PRO v15 - AI Music Video Director")
        self.setMinimumSize(1600, 900)
        
        # State
        self.user_credits = 47
        self.user_name = "Demo User"
        self.audio_file = None
        self.audio_duration = 0
        self.video_clips = []
        self.current_preset = 'balanced'
        self.lip_sync_model = None
        
        self.setup_ui()
        self.apply_styles()
        self.update_cost_display()
    
    def setup_ui(self):
        """Build complete UI"""
        self.create_menu_bar()
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top toolbar
        main_layout.addWidget(self.create_top_toolbar())
        
        # Main content
        content = QHBoxLayout()
        content.setSpacing(0)
        content.addWidget(self.create_left_sidebar())
        content.addWidget(self.create_center_area())
        content.addWidget(self.create_right_sidebar())
        main_layout.addLayout(content)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")
        main_layout.addWidget(self.status_bar)
    
    def create_center_area(self):
        """Center with video player"""
        center = QWidget()
        layout = QVBoxLayout(center)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Video player
        self.video_player = VideoPlayerWidget()
        layout.addWidget(self.video_player, 7)
        
        # Timeline/waveform area
        timeline = QLabel("Waveform • Beat Markers • Clip Timeline\n(Appears after generation)")
        timeline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timeline.setMinimumHeight(150)
        timeline.setStyleSheet("""
            background-color: #171717;
            border: 1px solid #3D3D3D;
            border-radius: 6px;
            color: #616161;
        """)
        layout.addWidget(timeline, 3)
        
        return center
    
    def create_right_sidebar(self):
        """Right sidebar with all controls"""
        sidebar = QWidget()
        sidebar.setFixedWidth(340)
        sidebar.setObjectName("rightSidebar")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # AI DIRECTOR
        header = QLabel("🤖 AI Director")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        
        # EDITING STYLE
        style_label = QLabel("Editing Intensity")
        style_label.setStyleSheet("font-size: 13px; font-weight: 600; margin-top: 8px;")
        layout.addWidget(style_label)
        
        for preset_key in ['chill', 'balanced', 'dynamic', 'flash_cuts', 'hypercut', 'extreme']:
            preset = EditingPresets.PRESETS[preset_key]
            btn = self.create_preset_button(preset_key, preset)
            layout.addWidget(btn)
        
        layout.addWidget(self.create_divider())
        
        # GENERATION SETTINGS
        settings_label = QLabel("Generation Settings")
        settings_label.setStyleSheet("font-size: 13px; font-weight: 600;")
        layout.addWidget(settings_label)
        
        # Quality
        quality_row = QHBoxLayout()
        quality_row.addWidget(QLabel("Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["720p", "1080p", "4K"])
        self.quality_combo.setCurrentIndex(1)
        quality_row.addWidget(self.quality_combo)
        layout.addLayout(quality_row)
        
        # Lip Sync Provider
        lipsync_label = QLabel("Lip Sync:")
        layout.addWidget(lipsync_label)
        
        self.lipsync_combo = QComboBox()
        self.lipsync_combo.addItems([
            "None (Faster, cheaper)",
            "Sync Labs ($0.05/sec)",
            "Rask AI ($1.50/min)"
        ])
        self.lipsync_combo.currentIndexChanged.connect(self.update_cost_display)
        layout.addWidget(self.lipsync_combo)
        
        layout.addStretch()
        
        # GENERATE BUTTON
        self.generate_btn = QPushButton("🎬 Generate Video")
        self.generate_btn.setFixedHeight(56)
        self.generate_btn.setObjectName("generateButton")
        self.generate_btn.clicked.connect(self.generate_video)
        layout.addWidget(self.generate_btn)
        
        # Cost display
        self.cost_label = QLabel("Cost: 1 credit")
        self.cost_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cost_label.setStyleSheet("color: #9E9E9E; font-size: 12px;")
        layout.addWidget(self.cost_label)
        
        return sidebar
    
    def create_preset_button(self, preset_key, preset):
        """Create preset button"""
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setChecked(preset_key == 'balanced')
        btn.setFixedHeight(68)
        btn.setObjectName("presetButton")
        btn.clicked.connect(lambda: self.select_preset(preset_key))
        
        layout = QHBoxLayout(btn)
        layout.setContentsMargins(12, 8, 12, 8)
        
        icon = QLabel(preset['icon'])
        icon.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        name_label = QLabel(preset['name'])
        name_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        text_layout.addWidget(name_label)
        
        desc_label = QLabel(preset['description'])
        desc_label.setStyleSheet("font-size: 11px; color: #9E9E9E;")
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)
        
        layout.addLayout(text_layout)
        
        return btn
    
    def select_preset(self, preset_key):
        """Select editing preset"""
        self.current_preset = preset_key
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == "presetButton":
                btn.setChecked(False)
        self.sender().setChecked(True)
    
    def update_cost_display(self):
        """Update credit cost in real-time"""
        lipsync_idx = self.lipsync_combo.currentIndex()
        lipsync_model = None
        if lipsync_idx == 1:
            lipsync_model = "sync_labs"
        elif lipsync_idx == 2:
            lipsync_model = "rask_ai"
        
        credits = CreditCalculator.calculate(
            len(self.video_clips),
            self.audio_duration,
            lipsync_model
        )
        
        self.cost_label.setText(f"Cost: {credits} credit{'s' if credits > 1 else ''}")
        
        # Show warning if insufficient credits
        if credits > self.user_credits:
            self.cost_label.setStyleSheet("color: #F44336; font-weight: bold;")
        else:
            self.cost_label.setStyleSheet("color: #4CAF50; font-size: 12px;")
    
    def generate_video(self):
        """Start video generation"""
        self.video_player.start_generation(len(self.video_clips))
        # Connect to actual backend here
    
    def create_menu_bar(self):
        """Menu bar (simplified for brevity)"""
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Import Audio...", self.import_audio)
        file_menu.addAction("Import Videos...", self.import_videos)
        
    def create_top_toolbar(self):
        """Top toolbar (simplified)"""
        toolbar = QWidget()
        toolbar.setFixedHeight(48)
        layout = QHBoxLayout(toolbar)
        
        logo = QLabel("BeatSync PRO")
        logo.setStyleSheet("font-weight: bold; color: #1E90FF;")
        layout.addWidget(logo)
        layout.addStretch()
        
        credits_label = QLabel(f"💳 {self.user_credits} Credits")
        layout.addWidget(credits_label)
        
        return toolbar
    
    def create_left_sidebar(self):
        """Left sidebar (simplified)"""
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        layout = QVBoxLayout(sidebar)
        
        # Audio section
        audio_btn = QPushButton("🎵 Import Audio")
        audio_btn.setFixedHeight(44)
        layout.addWidget(audio_btn)
        
        self.audio_info = QLabel("No audio (max 6 min)")
        self.audio_info.setStyleSheet("color: #616161; font-size: 12px;")
        layout.addWidget(self.audio_info)
        
        # Video section
        video_btn = QPushButton("📁 Import Videos")
        video_btn.setFixedHeight(44)
        layout.addWidget(video_btn)
        
        self.clips_info = QLabel("0/300 clips (max 15s each)")
        self.clips_info.setStyleSheet("color: #616161; font-size: 12px;")
        layout.addWidget(self.clips_info)
        
        layout.addStretch()
        return sidebar
    
    def create_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        return line
    
    def import_audio(self): pass
    def import_videos(self): pass
    
    def apply_styles(self):
        """Apply complete stylesheet"""
        self.setStyleSheet("""
            QMainWindow { background-color: #1E1E1E; }
            QWidget { color: #E0E0E0; font-family: 'Segoe UI'; font-size: 13px; }
            QPushButton {
                background-color: #252525;
                border: 1px solid #3D3D3D;
                border-radius: 6px;
                padding: 8px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #2D2D2D; }
            #generateButton {
                background-color: #1E90FF;
                color: white;
                border: none;
                font-size: 15px;
            }
            #generateButton:hover { background-color: #4169E1; }
            #presetButton { text-align: left; }
            #presetButton:checked {
                background-color: #1873CC;
                border-color: #1E90FF;
            }
            #playButton {
                background-color: #1E90FF;
                color: white;
                font-size: 16px;
                border-radius: 20px;
            }
            #timelineSlider::groove:horizontal {
                height: 6px;
                background: #2D2D2D;
                border-radius: 3px;
            }
            #timelineSlider::handle:horizontal {
                width: 14px;
                height: 14px;
                background: #1E90FF;
                border-radius: 7px;
                margin: -4px 0;
            }
            #playerControls {
                background-color: #171717;
                border-top: 1px solid #3D3D3D;
            }
        """)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = BeatSyncProMainWindow()
    window.show()
    sys.exit(app.exec())
