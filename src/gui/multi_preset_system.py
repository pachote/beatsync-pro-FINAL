"""
BEATSYNC PRO - MULTI-DIMENSIONAL PRESET SYSTEM
Revolutionary 5-tier preset system allowing simultaneous selection across categories
Users can mix and match presets from different categories for ultimate creative control
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QRadioButton, QCheckBox, QButtonGroup, QFrame)
from PySide6.QtCore import Qt, Signal

try:
    from .cinema_colors import CinemaColors as Colors
except ImportError:
    class Colors:
        BG_CARD = "#212936"
        BG_ELEVATED = "#1C2230"
        NEON_CYAN = "#00D9FF"
        TEXT_PRIMARY = "#FFFFFF"
        TEXT_SECONDARY = "#B8C5D0"
        TEXT_TERTIARY = "#8A95A0"
        BORDER = "#2F3541"


# ═══════════════════════════════════════════════════════════
# PRESET DATA DEFINITIONS
# ═══════════════════════════════════════════════════════════

EDITING_INTENSITY_PRESETS = {
    'chill': {
        'name': 'Chill',
        'description': 'Contemplative flow - AGI maintains cinematic pacing with strategic long cuts',
        'cuts_per_minute': (8, 12),
        'clip_mix': {'short': 0.20, 'medium': 0.30, 'long': 0.50},
        'avg_clip_duration': 6.0,
        'icon': '🌊'
    },
    'balanced': {
        'name': 'Balanced',
        'description': 'Perfect blend - AGI orchestrates variety with intelligent pacing',
        'cuts_per_minute': (15, 25),
        'clip_mix': {'short': 0.40, 'medium': 0.40, 'long': 0.20},
        'avg_clip_duration': 3.5,
        'icon': '⚖️',
        'default': True
    },
    'dynamic': {
        'name': 'Dynamic',
        'description': 'Energetic variety - AGI mixes rapid cuts with strategic breathing room',
        'cuts_per_minute': (30, 45),
        'clip_mix': {'short': 0.60, 'medium': 0.30, 'long': 0.10},
        'avg_clip_duration': 2.0,
        'icon': '⚡'
    },
    'flash_cuts': {
        'name': 'Flash Cuts',
        'description': 'Rapid fire with genius pacing - AGI maintains flow despite speed',
        'cuts_per_minute': (50, 70),
        'clip_mix': {'short': 0.75, 'medium': 0.20, 'long': 0.05},
        'avg_clip_duration': 1.0,
        'icon': '💥'
    },
    'hypercut': {
        'name': 'Hypercut',
        'description': 'Controlled chaos - AGI creates impossible complexity with strategic anchors',
        'cuts_per_minute': (80, 120),
        'clip_mix': {'short': 0.80, 'medium': 0.15, 'long': 0.05},
        'avg_clip_duration': 0.5,
        'icon': '🚀'
    },
    'extreme': {
        'name': 'EXTREME',
        'description': 'AGI GENIUS MODE - 70% ultra-short, 20% strategic pauses, 10% emotional anchors',
        'cuts_per_minute': (150, 200),
        'clip_mix': {'ultra_short': 0.70, 'medium': 0.20, 'anchor': 0.10},
        'avg_clip_duration': 0.3,
        'icon': '🔥'
    }
}

COLOR_GRADING_PRESETS = {
    'natural': {
        'name': 'Natural',
        'description': 'Clean, unprocessed look',
        'ffmpeg_filter': 'eq=saturation=1.0',
        'icon': '🌿'
    },
    'cinematic': {
        'name': 'Cinematic',
        'description': 'Film-grade color science (teal & orange)',
        'ffmpeg_filter': "eq=contrast=1.15:saturation=0.9,curves=all='0/0 0.25/0.1 0.75/0.9 1/1'",
        'icon': '🎬'
    },
    'vintage': {
        'name': 'Vintage',
        'description': 'Retro analog warmth (70s/80s film)',
        'ffmpeg_filter': 'eq=saturation=0.85,noise=c0s=7:allf=t,vignette=angle=PI/3',
        'icon': '📼'
    },
    'bleach_bypass': {
        'name': 'Bleach Bypass',
        'description': 'Desaturated high contrast',
        'ffmpeg_filter': "eq=saturation=0.5:contrast=1.4,curves=all='0/0 0.3/0.2 0.7/0.8 1/1'",
        'icon': '🏴'
    },
    'moody': {
        'name': 'Moody',
        'description': 'Dark, atmospheric (lifted blacks)',
        'ffmpeg_filter': "eq=brightness=-0.3:saturation=1.15,curves=all='0/0.1 0.3/0.2 0.7/0.7 1/1'",
        'icon': '🌙'
    },
    'vibrant': {
        'name': 'Vibrant',
        'description': 'Punchy saturated colors',
        'ffmpeg_filter': 'eq=saturation=1.4:contrast=1.1',
        'icon': '🌈'
    },
    'monochrome': {
        'name': 'Monochrome',
        'description': 'Black & white',
        'ffmpeg_filter': 'eq=saturation=0:contrast=1.2',
        'icon': '⬛'
    },
    'neon': {
        'name': 'Neon',
        'description': 'Cyberpunk aesthetics',
        'ffmpeg_filter': "eq=saturation=1.6:contrast=1.3,curves=all='0/0.2 0.5/0.5 1/0.9'",
        'icon': '💠'
    },
    'pastel': {
        'name': 'Pastel',
        'description': 'Soft dreamy colors',
        'ffmpeg_filter': "eq=saturation=0.7,curves=all='0/0.15 0.5/0.5 1/0.95'",
        'icon': '🎨'
    }
}

EFFECTS_PRESETS = {
    'clean': {
        'name': 'Clean',
        'description': 'No effects',
        'effects_list': [],
        'icon': '✨'
    },
    'subtle': {
        'name': 'Subtle',
        'description': 'Light enhancement',
        'effects_list': ['sharpen_light', 'slight_vignette'],
        'icon': '🔆'
    },
    'cinematic': {
        'name': 'Cinematic',
        'description': 'Film-grade effects (grain, flares, letterbox)',
        'effects_list': ['film_grain', 'lens_flare', 'letterbox_2_35'],
        'icon': '🎥'
    },
    'music_video': {
        'name': 'Music Video',
        'description': 'Bold visual impact (color pops, beat flash)',
        'effects_list': ['color_pop', 'beat_flash', 'chromatic_aberration'],
        'icon': '🎵'
    },
    'glitch': {
        'name': 'Glitch',
        'description': 'Digital corruption (RGB split, datamosh)',
        'effects_list': ['rgb_split', 'datamosh', 'scanlines'],
        'icon': '📺'
    },
    'retro': {
        'name': 'Retro',
        'description': 'VHS & 80s vibes (tracking errors, scanlines)',
        'effects_list': ['vhs_effect', 'tracking_errors', 'chroma_bleed'],
        'icon': '📹'
    },
    'psychedelic': {
        'name': 'Psychedelic',
        'description': 'Trippy visuals (kaleidoscope, trails)',
        'effects_list': ['kaleidoscope', 'motion_trails', 'color_shift'],
        'icon': '🌀'
    },
    'anime': {
        'name': 'Anime',
        'description': 'Animation effects (posterize, cel-shading)',
        'effects_list': ['posterize', 'cel_shading', 'outline_enhance'],
        'icon': '🎴'
    }
}

TRANSITION_PRESETS = {
    'cuts_only': {
        'name': 'Cuts Only',
        'description': 'Direct cuts (fast-paced)',
        'transition_type': 'cut',
        'icon': '✂️'
    },
    'dissolves': {
        'name': 'Dissolves',
        'description': 'Smooth crossfades',
        'transition_type': 'dissolve',
        'duration': 0.5,
        'icon': '🌫️'
    },
    'wipes': {
        'name': 'Wipes',
        'description': 'Directional transitions',
        'transition_type': 'wipe',
        'duration': 0.3,
        'icon': '↔️'
    },
    'zoom': {
        'name': 'Zoom',
        'description': 'Scale in/out transitions',
        'transition_type': 'zoom',
        'duration': 0.4,
        'icon': '🔍'
    },
    'spin': {
        'name': 'Spin',
        'description': 'Rotational effects',
        'transition_type': 'spin',
        'duration': 0.4,
        'icon': '🔄'
    },
    'glitch_transitions': {
        'name': 'Glitch',
        'description': 'Digital distortions',
        'transition_type': 'glitch',
        'duration': 0.2,
        'icon': '⚡'
    },
    'beat_synced': {
        'name': 'Beat-Synced',
        'description': 'Flash on every beat',
        'transition_type': 'beat_flash',
        'icon': '🥁'
    },
    'creative': {
        'name': 'Creative',
        'description': 'AI picks best transition',
        'transition_type': 'ai_select',
        'icon': '🎲'
    }
}

SPEED_PRESETS = {
    'constant': {
        'name': 'Constant',
        'description': 'Normal playback (1.0x all clips)',
        'speed_variations': False,
        'icon': '▶️'
    },
    'dynamic': {
        'name': 'Dynamic',
        'description': 'Auto speed variations (energy-based)',
        'speed_variations': True,
        'fast_percentage': 0.10,
        'slow_percentage': 0.05,
        'icon': '🎢'
    },
    'slow_motion': {
        'name': 'Slow Motion',
        'description': 'Dramatic slow-mo at peaks',
        'speed_variations': True,
        'slow_percentage': 0.20,
        'icon': '🐌'
    },
    'time_remap': {
        'name': 'Time Remap',
        'description': 'Complex speed curves',
        'speed_variations': True,
        'use_curves': True,
        'icon': '📈'
    },
    'beat_sync_speed': {
        'name': 'Beat-Sync Speed',
        'description': 'Tempo-locked ramping',
        'speed_variations': True,
        'sync_to_beats': True,
        'icon': '🎵'
    },
    'reverse': {
        'name': 'Reverse',
        'description': 'Strategic reverse sections',
        'reverse_percentage': 0.10,
        'icon': '⏪'
    }
}


# ═══════════════════════════════════════════════════════════
# PRESET SELECTION WIDGETS
# ═══════════════════════════════════════════════════════════

class PresetCategoryWidget(QWidget):
    """
    Base widget for a preset category (with radio buttons or checkboxes)
    """
    selection_changed = Signal(str, str)  # (category_name, preset_id)
    
    def __init__(self, category_name, presets_dict, selection_type='radio', parent=None):
        super().__init__(parent)
        
        self.category_name = category_name
        self.presets = presets_dict
        self.selection_type = selection_type  # 'radio' or 'checkbox'
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header
        header = QLabel(self.category_name)
        header.setStyleSheet(f"""
            font-size: 13px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
            padding-bottom: 4px;
        """)
        layout.addWidget(header)
        
        # Required/Optional indicator
        requirement = "REQUIRED" if self.selection_type == 'radio' else "Optional"
        req_label = QLabel(requirement)
        req_label.setStyleSheet(f"""
            font-size: 10px;
            color: {Colors.TEXT_TERTIARY};
            padding-bottom: 8px;
        """)
        layout.addWidget(req_label)
        
        # Buttons
        if self.selection_type == 'radio':
            self.button_group = QButtonGroup(self)
            self.button_group.buttonClicked.connect(self._on_radio_clicked)
        
        self.buttons = {}
        
        for preset_id, preset_data in self.presets.items():
            button_widget = self._create_preset_button(preset_id, preset_data)
            layout.addWidget(button_widget)
            
        layout.addStretch()
        
        # Style the container
        self.setStyleSheet(f"""
            PresetCategoryWidget {{
                background: {Colors.BG_CARD};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
            }}
        """)
    
    def _create_preset_button(self, preset_id, preset_data):
        """Create a single preset button"""
        container = QWidget()
        h_layout = QHBoxLayout(container)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(8)
        
        # Radio button or checkbox
        if self.selection_type == 'radio':
            button = QRadioButton()
            self.button_group.addButton(button)
            
            # Set default selection
            if preset_data.get('default', False):
                button.setChecked(True)
        else:
            button = QCheckBox()
            button.stateChanged.connect(
                lambda state, pid=preset_id: self._on_checkbox_changed(pid, state)
            )
        
        self.buttons[preset_id] = button
        h_layout.addWidget(button)
        
        # Icon (optional)
        if 'icon' in preset_data:
            icon_label = QLabel(preset_data['icon'])
            icon_label.setStyleSheet("font-size: 16px;")
            h_layout.addWidget(icon_label)
        
        # Text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        name_label = QLabel(preset_data['name'])
        name_label.setStyleSheet(f"""
            font-size: 12px;
            font-weight: 500;
            color: {Colors.TEXT_PRIMARY};
        """)
        text_layout.addWidget(name_label)
        
        desc_label = QLabel(preset_data['description'])
        desc_label.setStyleSheet(f"""
            font-size: 10px;
            color: {Colors.TEXT_SECONDARY};
        """)
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)
        
        h_layout.addLayout(text_layout, 1)
        
        # Style button
        button.setStyleSheet(f"""
            QRadioButton, QCheckBox {{
                spacing: 5px;
            }}
            QRadioButton::indicator, QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid {Colors.BORDER};
                background: {Colors.BG_ELEVATED};
            }}
            QRadioButton::indicator:checked, QCheckBox::indicator:checked {{
                background: {Colors.NEON_CYAN};
                border: 2px solid {Colors.NEON_CYAN};
            }}
            QRadioButton::indicator:hover, QCheckBox::indicator:hover {{
                border: 2px solid {Colors.NEON_CYAN};
            }}
        """)
        
        return container
    
    def _on_radio_clicked(self, button):
        """Handle radio button click"""
        for preset_id, btn in self.buttons.items():
            if btn == button:
                self.selection_changed.emit(self.category_name, preset_id)
                break
    
    def _on_checkbox_changed(self, preset_id, state):
        """Handle checkbox state change"""
        if state == Qt.CheckState.Checked.value:
            self.selection_changed.emit(self.category_name, preset_id)
        else:
            self.selection_changed.emit(self.category_name, None)
    
    def get_selected(self):
        """Get currently selected preset(s)"""
        if self.selection_type == 'radio':
            for preset_id, button in self.buttons.items():
                if button.isChecked():
                    return preset_id
            return None
        else:  # checkbox
            selected = []
            for preset_id, button in self.buttons.items():
                if button.isChecked():
                    selected.append(preset_id)
            return selected if selected else None


class MultiPresetSelector(QWidget):
    """
    ULTIMATE MULTI-DIMENSIONAL PRESET SELECTOR
    Allows users to combine presets from 5 different categories simultaneously
    """
    presets_changed = Signal(dict)  # Emits dict of all selected presets
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.category_widgets = {}
        self.current_selections = {
            'editing_intensity': 'balanced',  # Default
            'color_grading': None,
            'effects': None,
            'transitions': None,
            'speed': None
        }
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the multi-preset UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("🎨 CREATIVE PRESETS")
        title.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
            padding: 8px 0;
        """)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Mix and match presets from different categories")
        subtitle.setStyleSheet(f"""
            font-size: 11px;
            color: {Colors.TEXT_SECONDARY};
            padding-bottom: 12px;
        """)
        layout.addWidget(subtitle)
        
        # Category 1: Editing Intensity (REQUIRED - Radio)
        editing_widget = PresetCategoryWidget(
            "EDITING INTENSITY",
            EDITING_INTENSITY_PRESETS,
            selection_type='radio'
        )
        editing_widget.selection_changed.connect(self._on_selection_changed)
        self.category_widgets['editing_intensity'] = editing_widget
        layout.addWidget(editing_widget)
        
        # Category 2: Color Grading (OPTIONAL - Checkbox)
        color_widget = PresetCategoryWidget(
            "COLOR GRADING",
            COLOR_GRADING_PRESETS,
            selection_type='checkbox'
        )
        color_widget.selection_changed.connect(self._on_selection_changed)
        self.category_widgets['color_grading'] = color_widget
        layout.addWidget(color_widget)
        
        # Category 3: Effects (OPTIONAL - Checkbox)
        effects_widget = PresetCategoryWidget(
            "EFFECTS",
            EFFECTS_PRESETS,
            selection_type='checkbox'
        )
        effects_widget.selection_changed.connect(self._on_selection_changed)
        self.category_widgets['effects'] = effects_widget
        layout.addWidget(effects_widget)
        
        # Category 4: Transitions (OPTIONAL - Checkbox)
        transitions_widget = PresetCategoryWidget(
            "TRANSITIONS",
            TRANSITION_PRESETS,
            selection_type='checkbox'
        )
        transitions_widget.selection_changed.connect(self._on_selection_changed)
        self.category_widgets['transitions'] = transitions_widget
        layout.addWidget(transitions_widget)
        
        # Category 5: Speed (OPTIONAL - Checkbox)
        speed_widget = PresetCategoryWidget(
            "SPEED RAMPING",
            SPEED_PRESETS,
            selection_type='checkbox'
        )
        speed_widget.selection_changed.connect(self._on_selection_changed)
        self.category_widgets['speed'] = speed_widget
        layout.addWidget(speed_widget)
        
        layout.addStretch()
    
    def _on_selection_changed(self, category_name, preset_id):
        """Handle preset selection change"""
        # Update current selections
        category_key = category_name.lower().replace(' ', '_')
        self.current_selections[category_key] = preset_id
        
        # Emit combined selections
        self.presets_changed.emit(self.current_selections.copy())
    
    def get_all_selections(self):
        """Get all current preset selections"""
        return self.current_selections.copy()
    
    def get_preset_config(self):
        """
        Get complete preset configuration with all details
        
        Returns:
            dict: Complete configuration for video generation
        """
        config = {}
        
        # Editing intensity
        if self.current_selections['editing_intensity']:
            config['editing'] = EDITING_INTENSITY_PRESETS[
                self.current_selections['editing_intensity']
            ]
        
        # Color grading
        if self.current_selections['color_grading']:
            config['color_grading'] = COLOR_GRADING_PRESETS[
                self.current_selections['color_grading']
            ]
        
        # Effects
        if self.current_selections['effects']:
            config['effects'] = EFFECTS_PRESETS[
                self.current_selections['effects']
            ]
        
        # Transitions
        if self.current_selections['transitions']:
            config['transitions'] = TRANSITION_PRESETS[
                self.current_selections['transitions']
            ]
        
        # Speed
        if self.current_selections['speed']:
            config['speed'] = SPEED_PRESETS[
                self.current_selections['speed']
            ]
        
        return config
