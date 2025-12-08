from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QTextBrowser
from PySide6.QtCore import Qt

class ProColors:
    BG_DEEP = '#1a1a1a'
    BG_PANEL = '#242424'
    TEXT = '#e0e0e0'
    TEXT_DIM = '#888888'
    PRIMARY = '#00d4ff'
    ACCENT = '#00ff88'

def show_credits_dialog(parent):
    dialog = QDialog(parent)
    dialog.setWindowTitle('Account Credits')
    dialog.setModal(True)
    dialog.setFixedSize(450, 300)
    
    layout = QVBoxLayout(dialog)
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)
    
    # Title
    title = QLabel('💳 Account Credits')
    title.setStyleSheet(f'font-size: 20px; font-weight: bold; color: {ProColors.PRIMARY};')
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)
    
    # Credits balance
    balance = QLabel('47 credits')
    balance.setStyleSheet(f'font-size: 32px; font-weight: bold; color: {ProColors.ACCENT};')
    balance.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(balance)
    
    # Info
    info = QLabel('Credits are used for:\n\n• AI Video Generation: 1 credit per video\n• GPU-Accelerated Rendering: Included')
    info.setStyleSheet(f'font-size: 14px; color: {ProColors.TEXT}; padding: 15px; line-height: 1.6;')
    info.setAlignment(Qt.AlignmentFlag.AlignLeft)
    layout.addWidget(info)
    
    # Upgrade button
    upgrade_btn = QPushButton('Upgrade Subscription')
    upgrade_btn.setStyleSheet(f'''
        QPushButton {{
            background: {ProColors.PRIMARY};
            color: white;
            padding: 12px 30px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background: #00b8e6;
        }}
    ''')
    upgrade_btn.clicked.connect(lambda: dialog.accept())
    layout.addWidget(upgrade_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    dialog.setStyleSheet(f'''
        QDialog {{
            background: {ProColors.BG_DEEP};
            border-radius: 12px;
        }}
    ''')
    dialog.exec()

def show_quickstart_dialog(parent):
    dialog = QDialog(parent)
    dialog.setWindowTitle('Quick Start Guide')
    dialog.setModal(True)
    dialog.setFixedSize(650, 550)
    
    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(30, 30, 30, 30)
    
    # Title
    title = QLabel('🚀 Quick Start Guide')
    title.setStyleSheet(f'font-size: 20px; font-weight: bold; color: {ProColors.PRIMARY};')
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)
    
    # Content
    content = QTextBrowser()
    content.setOpenExternalLinks(False)
    content.setHtml(f'''
    <style>
        body {{ color: {ProColors.TEXT}; font-size: 14px; line-height: 1.8; }}
        h2 {{ color: {ProColors.PRIMARY}; font-size: 16px; margin-top: 20px; }}
        ul {{ margin-left: 20px; }}
    </style>
    <h2>STEP 1: Import Your Music</h2>
    <ul>
        <li>Click "+ Import Audio" button in left panel</li>
        <li>Select your music file (MP3, WAV, FLAC)</li>
        <li>BeatSync will auto-analyze beats and energy</li>
    </ul>
    
    <h2>STEP 2: Add Video Clips</h2>
    <ul>
        <li>Click "+ Import Videos" button</li>
        <li>Select 10-50 video clips (3-15 seconds each)</li>
        <li>More clips = better variety and AI choices</li>
    </ul>
    
    <h2>STEP 3: Choose Editing Style</h2>
    <ul>
        <li>Select preset: Balanced, Dynamic, Flash Cuts, or EXTREME</li>
        <li>Toggle effects: Beat Flash, Saturation Pulse, Camera Shake</li>
    </ul>
    
    <h2>STEP 4: Generate Your Video!</h2>
    <ul>
        <li>Click "Generate Video" button</li>
        <li>AGI Director creates your music video (30-120 seconds)</li>
        <li>Video saves to: C:\\Users\\pacho\\Videos\\BeatSync PRO</li>
    </ul>
    
    <p style="margin-top: 20px; color: {ProColors.TEXT_DIM};">
        <b>Pro Tip:</b> Use high-quality 1080p or 4K video clips for best results!
    </p>
    ''')
    content.setStyleSheet(f'''
        QTextBrowser {{
            background: {ProColors.BG_PANEL};
            border: 1px solid #333;
            border-radius: 8px;
            padding: 15px;
        }}
    ''')
    layout.addWidget(content)
    
    # Button
    ok_btn = QPushButton('Got it!')
    ok_btn.setStyleSheet(f'''
        QPushButton {{
            background: {ProColors.PRIMARY};
            color: white;
            padding: 12px 40px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background: #00b8e6;
        }}
    ''')
    ok_btn.clicked.connect(dialog.accept)
    layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    dialog.setStyleSheet(f'''
        QDialog {{
            background: {ProColors.BG_DEEP};
            border-radius: 12px;
        }}
    ''')
    dialog.exec()

def show_about_dialog(parent):
    dialog = QDialog(parent)
    dialog.setWindowTitle('About BeatSync PRO')
    dialog.setModal(True)
    dialog.setFixedSize(500, 450)
    
    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(40, 40, 40, 40)
    layout.setSpacing(20)
    
    # Logo/Icon
    logo = QLabel('🎵')
    logo.setStyleSheet('font-size: 64px;')
    logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(logo)
    
    # Title
    title = QLabel('BeatSync PRO')
    title.setStyleSheet(f'font-size: 28px; font-weight: bold; color: {ProColors.PRIMARY};')
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)
    
    # Version
    version = QLabel('Version 1.0.0')
    version.setStyleSheet(f'font-size: 12px; color: {ProColors.TEXT_DIM};')
    version.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(version)
    
    layout.addSpacing(10)
    
    # Info
    info = QLabel('''AI-Powered Music Video Creation
    
- Millisecond-precise beat synchronization
- AGI Director for intelligent editing
- Professional effects & transitions
- GPU-accelerated rendering

© 2025 RendereelStudio LLC
Created by Christopher Wheeler

Portland, Oregon''')
    info.setWordWrap(True)
    info.setStyleSheet(f'font-size: 14px; color: {ProColors.TEXT}; line-height: 1.8;')
    info.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(info)
    
    # Website link
    website = QLabel('<a href="https://beatsyncpro.ai" style="color: #00d4ff; text-decoration: none;">beatsyncpro.ai</a>')
    website.setTextFormat(Qt.TextFormat.RichText)
    website.setOpenExternalLinks(True)
    website.setStyleSheet('font-size: 14px;')
    website.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(website)
    
    layout.addSpacing(10)
    
    # Close button
    close_btn = QPushButton('Close')
    close_btn.setStyleSheet(f'''
        QPushButton {{
            background: {ProColors.PRIMARY};
            color: white;
            padding: 12px 40px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background: #00b8e6;
        }}
    ''')
    close_btn.clicked.connect(dialog.accept)
    layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    dialog.setStyleSheet(f'''
        QDialog {{
            background: {ProColors.BG_DEEP};
            border-radius: 12px;
        }}
    ''')
    dialog.exec()
