from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class CompactPresetSelector(QWidget):
    """Clean collapsible preset system - only ONE category open at a time"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_selections = {
            "editing": "Balanced",
            "color": "Natural", 
            "effects": "Clean",
            "transitions": "Cuts Only",
            "speed": "Constant"
        }
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Create compact category buttons
        categories = [
            ("EDITING", "editing", ["Chill", "Balanced", "Dynamic", "Flash Cuts", "Hypercut", "EXTREME"]),
            ("COLOR", "color", ["Natural", "Cinematic", "Vintage", "Vibrant", "Monochrome", "Neon", "Pastel", "Cyberpunk", "Film Noir"]),
            ("EFFECTS", "effects", ["Clean", "Subtle", "Cinematic", "Music Video", "Experimental", "Glitch", "Retro", "Glitch Storm"]),
            ("TRANSITIONS", "transitions", ["Cuts Only", "Dissolves", "Wipes", "Zoom", "Spin", "Glitch", "Beat-Synced", "Morphing"]),
            ("SPEED", "speed", ["Constant", "Dynamic", "Slow Motion", "Time Remap", "Beat-Sync Speed", "Reverse"])
        ]
        
        self.category_widgets = {}
        
        for title, key, options in categories:
            # Category button (shows current selection)
            btn = QPushButton(f"{title}: {self.current_selections[key]}")
            btn.setFixedHeight(36)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: #1C2230;
                    color: #B8C5D0;
                    border: 1px solid #2F3541;
                    border-radius: 6px;
                    padding: 0 12px;
                    text-align: left;
                    font-size: 11px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background: #212936;
                    border: 1px solid #00D9FF;
                    color: #00D9FF;
                }}
            """)
            btn.clicked.connect(lambda checked, k=key, opts=options, b=btn: self.toggle_category(k, opts, b))
            layout.addWidget(btn)
            self.category_widgets[key] = {"button": btn, "expanded": False}
        
        layout.addStretch()
    
    def toggle_category(self, key, options, button):
        # Close all other categories first
        for k, w in self.category_widgets.items():
            if k != key and w["expanded"]:
                # Remove dropdown if exists
                pass
        
        # Show dropdown menu
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background: #0F1419;
                border: 1px solid #00D9FF;
                border-radius: 6px;
                padding: 4px;
            }}
            QMenu::item {{
                background: transparent;
                color: #B8C5D0;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background: #1C2230;
                color: #00D9FF;
            }}
        """)
        
        for option in options:
            action = menu.addAction(option)
            if option == self.current_selections[key]:
                action.setCheckable(True)
                action.setChecked(True)
            action.triggered.connect(lambda checked, o=option, k=key, b=button: self.select_option(k, o, b))
        
        # Show menu below button
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec(pos)
    
    def select_option(self, key, option, button):
        self.current_selections[key] = option
        # Update button text
        category_names = {"editing": "EDITING", "color": "COLOR", "effects": "EFFECTS", 
                         "transitions": "TRANSITIONS", "speed": "SPEED"}
        button.setText(f"{category_names[key]}: {option}")
