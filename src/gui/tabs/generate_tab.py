"""
Generate/export tab for BeatSync PRO.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class GenerateTab(QWidget):
    """Generate/export tab."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()
        
        # Placeholder content
        label = QLabel("Generate & Export - Coming Soon")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 24px;
                padding: 50px;
            }
        """)
        
        layout.addWidget(label)
        layout.addStretch()
        
        self.setLayout(layout)