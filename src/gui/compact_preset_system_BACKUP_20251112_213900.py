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
            "effects": "Static Camera",
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
            ("COLOR GRADING", "color", ["Natural", "Cinematic Look", "Cyberpunk Neon", "Vintage Film", "High Contrast B&W", "Neon Dream", "Warm Sunset", "Cool Blue"]),
            ("CAMERA MOTION", "effects", ["Static Camera", "Smooth Zoom", "Intense Shake", "Subtle Pan"]),
            ("TRANSITIONS", "transitions", ["Cuts Only", "Flash", "Dissolve", "Zoom", "Slide", "Glitch"]),
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
        print(f"🔧 select_option CALLED: {key} = {option}")
        
        # Map user-friendly names to backend names
        backend_map = {
            "Cinematic Look": "Cinematic",
            "Cyberpunk Neon": "Cyberpunk",
            "Vintage Film": "Vintage",
            "High Contrast B&W": "High Contrast",
            "Neon Dream": "Neon Dream",
            "Warm Sunset": "Warm Sunset",
            "Cool Blue": "Cool Blue",
            "Static Camera": "Clean",
            "Smooth Zoom": "Subtle",
            "Intense Shake": "Glitch Storm",
            "Subtle Pan": "Cinematic"
        }
        
        # Convert to backend name if mapping exists, otherwise use as-is
        backend_value = backend_map.get(option, option)
        self.current_selections[key] = backend_value
        print(f"   → Backend value: {backend_value}")
        # Update button text
        category_names = {"editing": "EDITING", "color": "COLOR", "effects": "EFFECTS", 
                         "transitions": "TRANSITIONS", "speed": "SPEED"}
        button.setText(f"{category_names[key]}: {option}")
