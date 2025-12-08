"""
BEATSYNC PRO - PROFESSIONAL UI V2
Adobe Premiere Pro + Topaz Video AI inspired
Full menu bar, credit system, account integration
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Colors:
    # Professional dark theme (Adobe/Topaz style)
    BG_DARK = "#1E1E1E"          # Main background
    BG_DARKER = "#171717"        # Panels
    BG_ELEVATED = "#252525"      # Cards
    BG_INPUT = "#2D2D2D"         # Input fields
    
    ACCENT_BLUE = "#1E90FF"      # Primary actions
    ACCENT_BLUE_HOVER = "#4169E1"
    ACCENT_BLUE_DARK = "#1873CC"
    
    SUCCESS = "#4CAF50"
    WARNING = "#FFC107"
    ERROR = "#F44336"
    
    TEXT = "#E0E0E0"             # Primary text
    TEXT_DIM = "#9E9E9E"         # Secondary text
    TEXT_DISABLED = "#616161"
    
    BORDER = "#3D3D3D"
    BORDER_LIGHT = "#555555"
    DIVIDER = "#2D2D2D"

class BeatSyncProMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeatSync PRO v15 - AI Music Video Director")
        self.setMinimumSize(1600, 900)
        self.resize(1920, 1080)
        
        # User state
        self.user_credits = 47  # Demo credits
        self.user_name = "Demo User"
        self.current_project = None
        self.audio_file = None
        self.video_clips = []
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Build the complete UI"""
        # Menu bar
        self.create_menu_bar()
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top toolbar with account/credits
        main_layout.addWidget(self.create_top_toolbar())
        
        # Main content area
        content = QHBoxLayout()
        content.setSpacing(0)
        content.addWidget(self.create_left_sidebar())
        content.addWidget(self.create_center_area())
        content.addWidget(self.create_right_sidebar())
        main_layout.addLayout(content)
        
        # Bottom status bar
        main_layout.addWidget(self.create_status_bar())
    
    def create_menu_bar(self):
        """Professional menu bar"""
        menubar = self.menuBar()
        
        # FILE MENU
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Project", self.new_project, "Ctrl+N")
        file_menu.addAction("Open Project...", self.open_project, "Ctrl+O")
        file_menu.addAction("Save Project", self.save_project, "Ctrl+S")
        file_menu.addAction("Save Project As...", self.save_project_as, "Ctrl+Shift+S")
        file_menu.addSeparator()
        file_menu.addAction("Import Audio...", self.import_audio, "Ctrl+I")
        file_menu.addAction("Import Videos...", self.import_videos, "Ctrl+Shift+I")
        file_menu.addSeparator()
        file_menu.addAction("Export Video...", self.export_video, "Ctrl+E")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close, "Ctrl+Q")
        
        # EDIT MENU
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo", lambda: None, "Ctrl+Z")
        edit_menu.addAction("Redo", lambda: None, "Ctrl+Y")
        edit_menu.addSeparator()
        edit_menu.addAction("Preferences...", self.show_preferences, "Ctrl+,")
        
        # PROJECT MENU
        project_menu = menubar.addMenu("Project")
        project_menu.addAction("Project Settings...", self.project_settings)
        project_menu.addAction("Clear All Clips", self.clear_clips)
        
        # HELP MENU
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation", self.show_docs, "F1")
        help_menu.addAction("Keyboard Shortcuts", self.show_shortcuts)
        help_menu.addAction("Video Tutorials", self.show_tutorials)
        help_menu.addSeparator()
        help_menu.addAction("Check for Updates...", self.check_updates)
        help_menu.addAction("Report Bug...", self.report_bug)
        help_menu.addSeparator()
        help_menu.addAction("Terms of Service", self.show_terms)
        help_menu.addAction("Privacy Policy", self.show_privacy)
        help_menu.addAction("About BeatSync PRO", self.show_about)
    
    def create_top_toolbar(self):
        """Top toolbar with account and credits"""
        toolbar = QWidget()
        toolbar.setFixedHeight(48)
        toolbar.setObjectName("topToolbar")
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(16, 8, 16, 8)
        
        # Logo/Title
        logo_label = QLabel("BeatSync PRO")
        logo_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E90FF;")
        layout.addWidget(logo_label)
        
        layout.addStretch()
        
        # Credits display
        credits_widget = QWidget()
        credits_layout = QHBoxLayout(credits_widget)
        credits_layout.setContentsMargins(12, 4, 12, 4)
        credits_widget.setObjectName("creditsWidget")
        
        credits_icon = QLabel("💳")
        credits_layout.addWidget(credits_icon)
        
        credits_label = QLabel(f"{self.user_credits} Credits")
        credits_label.setStyleSheet("font-weight: 600; color: #4CAF50;")
        credits_layout.addWidget(credits_label)
        
        buy_btn = QPushButton("Buy More")
        buy_btn.setFixedHeight(28)
        buy_btn.clicked.connect(self.buy_credits)
        credits_layout.addWidget(buy_btn)
        
        layout.addWidget(credits_widget)
        
        # Account menu
        account_btn = QPushButton(f"👤 {self.user_name}")
        account_btn.setFixedHeight(32)
        account_menu = QMenu()
        account_menu.addAction("Account Settings", self.account_settings)
        account_menu.addAction("Subscription", self.manage_subscription)
        account_menu.addAction("Usage History", self.usage_history)
        account_menu.addSeparator()
        account_menu.addAction("Sign Out", self.sign_out)
        account_btn.setMenu(account_menu)
        layout.addWidget(account_btn)
        
        return toolbar
    
    def create_left_sidebar(self):
        """Left sidebar - Media library"""
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setObjectName("leftSidebar")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        # AUDIO SECTION
        audio_header = QLabel("Audio Track")
        audio_header.setStyleSheet("font-size: 14px; font-weight: 600;")
        layout.addWidget(audio_header)
        
        # Audio import button
        audio_import = QPushButton("🎵 Import Audio File")
        audio_import.setFixedHeight(44)
        audio_import.clicked.connect(self.import_audio)
        layout.addWidget(audio_import)
        
        # Audio info (when loaded)
        self.audio_info_label = QLabel("No audio loaded")
        self.audio_info_label.setWordWrap(True)
        self.audio_info_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 12px; padding: 8px;")
        layout.addWidget(self.audio_info_label)
        
        layout.addWidget(self.create_divider())
        
        # VIDEO LIBRARY SECTION
        video_header = QLabel(f"Video Library (0/300)")
        video_header.setStyleSheet("font-size: 14px; font-weight: 600;")
        layout.addWidget(video_header)
        self.video_header_label = video_header
        
        # Video import button
        video_import = QPushButton("📁 Import Videos")
        video_import.setFixedHeight(44)
        video_import.clicked.connect(self.import_videos)
        layout.addWidget(video_import)
        
        # Video list/grid
        self.video_list = QListWidget()
        self.video_list.setObjectName("videoList")
        layout.addWidget(self.video_list, 1)
        
        return sidebar
    
    def create_center_area(self):
        """Center preview and timeline"""
        center = QWidget()
        center.setObjectName("centerArea")
        
        layout = QVBoxLayout(center)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        # Video preview
        preview_label = QLabel("Preview")
        preview_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        layout.addWidget(preview_label)
        
        self.preview_widget = QLabel("No video loaded\n\nImport audio and videos to begin")
        self.preview_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_widget.setMinimumHeight(400)
        self.preview_widget.setObjectName("previewWidget")
        layout.addWidget(self.preview_widget, 6)
        
        # Timeline
        timeline_label = QLabel("Timeline")
        timeline_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        layout.addWidget(timeline_label)
        
        self.timeline_widget = QLabel("Timeline will appear here after generation\n\nWaveform • Beat Markers • Clips")
        self.timeline_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timeline_widget.setMinimumHeight(200)
        self.timeline_widget.setObjectName("timelineWidget")
        layout.addWidget(self.timeline_widget, 4)
        
        return center
    
    def create_right_sidebar(self):
        """Right sidebar - AI controls"""
        sidebar = QWidget()
        sidebar.setFixedWidth(320)
        sidebar.setObjectName("rightSidebar")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # AI DIRECTOR SECTION
        ai_header = QLabel("🤖 AI Director")
        ai_header.setStyleSheet("font-size: 16px; font-weight: 700;")
        layout.addWidget(ai_header)
        
        # Editing style presets
        style_label = QLabel("Editing Style")
        style_label.setStyleSheet("font-size: 13px; font-weight: 600; margin-top: 8px;")
        layout.addWidget(style_label)
        
        presets = [
            ("Chill", "30-40 clips • 3-5s each\nBallads, acoustic, ambient"),
            ("Balanced", "50-70 clips • 2-4s each\nMost genres • Recommended"),
            ("Dynamic", "80-100 clips • 1.5-3s each\nPop, rock, upbeat"),
            ("Flash Cuts", "120-150 clips • 0.5-1.5s each\nElectronic, EDM, fast"),
            ("Hypercut", "180-250 clips • 0.3-1s each\nExperimental, extreme"),
        ]
        
        self.preset_buttons = []
        for i, (name, desc) in enumerate(presets):
            btn = self.create_preset_button(name, desc, i == 1)
            layout.addWidget(btn)
            self.preset_buttons.append(btn)
        
        layout.addStretch()
        
        # Generation settings
        layout.addWidget(self.create_divider())
        
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
        
        # Lip sync toggle
        self.lipsync_check = QCheckBox("Enable Lip Sync (uses more credits)")
        self.lipsync_check.setStyleSheet("margin-top: 8px;")
        layout.addWidget(self.lipsync_check)
        
        # GENERATE BUTTON
        self.generate_btn = QPushButton("🎬 Generate Video")
        self.generate_btn.setFixedHeight(56)
        self.generate_btn.setObjectName("generateButton")
        self.generate_btn.clicked.connect(self.generate_video)
        layout.addWidget(self.generate_btn)
        
        # Cost estimate
        self.cost_label = QLabel("Cost: 1 credit")
        self.cost_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cost_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 12px; margin-top: 4px;")
        layout.addWidget(self.cost_label)
        
        return sidebar
    
    def create_preset_button(self, name, description, checked=False):
        """Create a professional preset button"""
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setFixedHeight(72)
        btn.setObjectName("presetButton")
        
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        layout.addWidget(name_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"font-size: 11px; color: {Colors.TEXT_DIM};")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return btn
    
    def create_status_bar(self):
        """Bottom status bar"""
        status = QStatusBar()
        status.setFixedHeight(32)
        status.showMessage("Ready")
        return status
    
    def create_divider(self):
        """Horizontal divider line"""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("divider")
        return line
    
    def apply_styles(self):
        """Apply complete stylesheet"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {Colors.BG_DARK};
            }}
            QWidget {{
                color: {Colors.TEXT};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }}
            QMenuBar {{
                background-color: {Colors.BG_DARKER};
                border-bottom: 1px solid {Colors.BORDER};
                padding: 4px;
            }}
            QMenuBar::item {{
                padding: 6px 12px;
                background-color: transparent;
            }}
            QMenuBar::item:selected {{
                background-color: {Colors.BG_ELEVATED};
            }}
            QMenu {{
                background-color: {Colors.BG_ELEVATED};
                border: 1px solid {Colors.BORDER};
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 24px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {Colors.ACCENT_BLUE};
            }}
            #topToolbar {{
                background-color: {Colors.BG_DARKER};
                border-bottom: 1px solid {Colors.BORDER};
            }}
            #creditsWidget {{
                background-color: {Colors.BG_ELEVATED};
                border-radius: 6px;
            }}
            #leftSidebar, #rightSidebar {{
                background-color: {Colors.BG_DARKER};
                border-right: 1px solid {Colors.BORDER};
            }}
            #centerArea {{
                background-color: {Colors.BG_DARK};
            }}
            #previewWidget, #timelineWidget {{
                background-color: {Colors.BG_DARKER};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
                color: {Colors.TEXT_DIM};
            }}
            #videoList {{
                background-color: {Colors.BG_ELEVATED};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
            }}
            #divider {{
                background-color: {Colors.BORDER};
                max-height: 1px;
            }}
            QPushButton {{
                background-color: {Colors.BG_ELEVATED};
                color: {Colors.TEXT};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_INPUT};
                border-color: {Colors.BORDER_LIGHT};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BORDER};
            }}
            #generateButton {{
                background-color: {Colors.ACCENT_BLUE};
                color: white;
                border: none;
                font-size: 15px;
                font-weight: 700;
            }}
            #generateButton:hover {{
                background-color: {Colors.ACCENT_BLUE_HOVER};
            }}
            #generateButton:pressed {{
                background-color: {Colors.ACCENT_BLUE_DARK};
            }}
            #presetButton {{
                background-color: {Colors.BG_ELEVATED};
                border: 2px solid {Colors.BORDER};
                text-align: left;
            }}
            #presetButton:checked {{
                background-color: {Colors.ACCENT_BLUE_DARK};
                border-color: {Colors.ACCENT_BLUE};
            }}
            QComboBox {{
                background-color: {Colors.BG_INPUT};
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QCheckBox {{
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {Colors.BORDER};
                border-radius: 3px;
                background-color: {Colors.BG_INPUT};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Colors.ACCENT_BLUE};
                border-color: {Colors.ACCENT_BLUE};
            }}
        """)
    
    # Menu Actions
    def new_project(self): QMessageBox.information(self, "New Project", "Create new project")
    def open_project(self): QMessageBox.information(self, "Open", "Open project")
    def save_project(self): QMessageBox.information(self, "Save", "Save project")
    def save_project_as(self): QMessageBox.information(self, "Save As", "Save project as")
    def import_audio(self): QMessageBox.information(self, "Import", "Import audio file")
    def import_videos(self): QMessageBox.information(self, "Import", "Import video files")
    def export_video(self): QMessageBox.information(self, "Export", "Export video")
    def show_preferences(self): QMessageBox.information(self, "Preferences", "App preferences")
    def project_settings(self): QMessageBox.information(self, "Settings", "Project settings")
    def clear_clips(self): self.video_list.clear()
    def show_docs(self): QMessageBox.information(self, "Help", "Documentation")
    def show_shortcuts(self): QMessageBox.information(self, "Shortcuts", "Keyboard shortcuts")
    def show_tutorials(self): QMessageBox.information(self, "Tutorials", "Video tutorials")
    def check_updates(self): QMessageBox.information(self, "Updates", "Check for updates")
    def report_bug(self): QMessageBox.information(self, "Bug Report", "Report a bug")
    def show_terms(self): QMessageBox.information(self, "Terms", "Terms of Service")
    def show_privacy(self): QMessageBox.information(self, "Privacy", "Privacy Policy")
    def show_about(self): QMessageBox.information(self, "About", "BeatSync PRO v15")
    def buy_credits(self): QMessageBox.information(self, "Credits", "Buy more credits")
    def account_settings(self): QMessageBox.information(self, "Account", "Account settings")
    def manage_subscription(self): QMessageBox.information(self, "Subscription", "Manage subscription")
    def usage_history(self): QMessageBox.information(self, "Usage", "Usage history")
    def sign_out(self): QMessageBox.information(self, "Sign Out", "Sign out")
    def generate_video(self): QMessageBox.information(self, "Generate", "Generate video")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = BeatSyncProMainWindow()
    window.show()
    sys.exit(app.exec())
