import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QGroupBox, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt, QSize, QThread, Signal
from PySide6.QtGui import QIcon
from utils.thumbnail_generator import ThumbnailWorker
from core.visual_intelligence_v2 import VisualIntelligenceV2

class ClickableLabel(QLabel):
    clicked = Signal(str)

    def __init__(self, text, bin_name):
        super().__init__(text)
        self.bin_name = bin_name
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('QLabel { padding: 3px; font-size: 11px; } QLabel:hover { background-color: #4a5568; border-radius: 3px; }')

    def mousePressEvent(self, event):
        self.clicked.emit(self.bin_name)

class AnalysisWorker(QThread):
    finished = Signal(str, dict)
    error = Signal(str, str)

    def __init__(self, video_path, analyzer):
        super().__init__()
        self.video_path = video_path
        self.analyzer = analyzer

    def run(self):
        try:
            analysis_data = self.analyzer.analyze_video(self.video_path)
            self.finished.emit(self.video_path, analysis_data)
        except Exception as e:
            self.error.emit(self.video_path, str(e))

class ImportTab(QWidget):
    def __init__(self, analyzer=None):
        super().__init__()
        self.analyzer = analyzer or VisualIntelligenceV2()
        self.video_files = {}
        self.analysis_data = {}
        self.workers = []
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        media_import_group = QGroupBox('Media Import Controls')
        media_import_layout = QHBoxLayout()
        self.import_button = QPushButton('Import Videos')
        self.import_button.clicked.connect(self.import_videos)
        self.reanalyze_button = QPushButton("Re-Analyze All Videos")
        self.reanalyze_button.clicked.connect(self.reanalyze_all_videos)
        self.debug_button = QPushButton("DEBUG: Print Analysis Data")
        self.debug_button.clicked.connect(lambda: print(f"📊 ANALYSIS DATA: {len(self.analysis_data)} videos stored"))
        self.imported_files_label = QLabel('Imported Files: 0')
        media_import_layout.addWidget(self.import_button)
        media_import_layout.addWidget(self.reanalyze_button)
        media_import_layout.addWidget(self.debug_button)
        media_import_layout.addWidget(self.imported_files_label)
        media_import_layout.addStretch()
        media_import_group.setLayout(media_import_layout)
        main_layout.addWidget(media_import_group)

        content_layout = QHBoxLayout()

        # CLEAN SMART BINS WITH SCROLL
        smart_bins_group = QGroupBox('Smart Bins')
        bins_main_layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        bins_container = QWidget()
        smart_bins_layout = QVBoxLayout(bins_container)
        
        self.bin_labels = {}
        
        # Helper for section headers
        def add_section(title):
            header = QLabel(title)
            header.setStyleSheet('font-weight: bold; color: #4299e1; margin-top: 6px; font-size: 10px;')
            smart_bins_layout.addWidget(header)
        
        # OVERVIEW
        self.bin_labels['Show All'] = ClickableLabel('?? All (0)', 'Show All')
        smart_bins_layout.addWidget(self.bin_labels['Show All'])
        
        # SUBJECT
        add_section('SUBJECT')
        bins = [('People', '??'), ('Nature', '??'), ('Urban', '???'), ('Objects', '??')]
        for name, emoji in bins:
            self.bin_labels[name] = ClickableLabel(f'{emoji} {name} (0)', name)
            smart_bins_layout.addWidget(self.bin_labels[name])
        
        # STYLE
        add_section('STYLE')
        bins = [('Photorealistic', '??'), ('CGI/3D', '??'), ('AI Generated', '??')]
        for name, emoji in bins:
            self.bin_labels[name] = ClickableLabel(f'{emoji} {name} (0)', name)
            smart_bins_layout.addWidget(self.bin_labels[name])
        
        # GENDER
        add_section('GENDER')
        bins = [('Male', '??'), ('Female', '??')]
        for name, emoji in bins:
            self.bin_labels[name] = ClickableLabel(f'{emoji} {name} (0)', name)
            smart_bins_layout.addWidget(self.bin_labels[name])
        
        # ENERGY
        add_section('ENERGY')
        bins = [('High Energy', '??'), ('Medium Energy', '??'), ('Low Energy', '??')]
        for name, emoji in bins:
            self.bin_labels[name] = ClickableLabel(f'{emoji} {name} (0)', name)
            smart_bins_layout.addWidget(self.bin_labels[name])
        
        # COLORS
        add_section('COLORS')
        bins = [('Warm Colors', '??'), ('Cool Colors', '??')]
        for name, emoji in bins:
            self.bin_labels[name] = ClickableLabel(f'{emoji} {name} (0)', name)
            smart_bins_layout.addWidget(self.bin_labels[name])
        
        # SPECIAL
        add_section('SPECIAL')
        self.bin_labels['Lip Sync Ready'] = ClickableLabel('?? Lip Sync (0)', 'Lip Sync Ready')
        smart_bins_layout.addWidget(self.bin_labels['Lip Sync Ready'])
        
        for label in self.bin_labels.values():
            label.clicked.connect(self._filter_media_bin)
        
        smart_bins_layout.addStretch()
        scroll.setWidget(bins_container)
        bins_main_layout.addWidget(scroll)
        smart_bins_group.setLayout(bins_main_layout)
        content_layout.addWidget(smart_bins_group, 1)

        media_bin_group = QGroupBox('Imported Media Bin')
        media_bin_layout = QVBoxLayout()
        self.media_list_widget = QListWidget()
        self.media_list_widget.setViewMode(QListWidget.IconMode)
        self.media_list_widget.setIconSize(QSize(128, 128))
        self.media_list_widget.setResizeMode(QListWidget.Adjust)
        media_bin_layout.addWidget(self.media_list_widget)
        media_bin_group.setLayout(media_bin_layout)
        content_layout.addWidget(media_bin_group, 4)

        main_layout.addLayout(content_layout)

    def import_videos(self):
        from PySide6.QtWidgets import QFileDialog
        video_paths, _ = QFileDialog.getOpenFileNames(self, 'Select Videos', '', 'Video Files (*.mp4 *.mov *.MOV)')
        if not video_paths: return

        self.imported_files_label.setText(f'Imported Files: {len(self.video_files) + len(video_paths)}')
        for video_path in video_paths:
            self.add_video_to_bin(video_path)
            self.start_analysis(video_path)

    def add_video_to_bin(self, video_path):
        item = QListWidgetItem(os.path.basename(video_path))
        item.setData(Qt.UserRole, video_path)
        item.setSizeHint(QSize(140, 140))
        self.media_list_widget.addItem(item)
        self.video_files[video_path] = item

        thumb_worker = ThumbnailWorker(video_path)
        thumb_worker.finished.connect(self.set_thumbnail)
        self.workers.append(thumb_worker)
        thumb_worker.start()

    def set_thumbnail(self, video_path, icon):
        if video_path in self.video_files:
            self.video_files[video_path].setIcon(icon)

    def start_analysis(self, video_path):
        worker = AnalysisWorker(video_path, self.analyzer)
        worker.finished.connect(self._on_analysis_complete)
        worker.error.connect(lambda path, err: print(f'[ERROR] {os.path.basename(path)}: {err}'))
        self.workers.append(worker)
        worker.start()

    def _on_analysis_complete(self, video_path, analysis_data):
        print(f'?? [IMPORT_TAB DEBUG] Storing analysis with key: "{video_path}"')
        self.analysis_data[video_path] = analysis_data
        print("⚡ About to call _update_smart_bins...")
        self._update_smart_bins()
        print("✅ _update_smart_bins returned successfully")
        
        subject = analysis_data.get('subject_type', '?')
        style = analysis_data.get('art_style', '?')
        energy = analysis_data.get('energy_level', 0)
        sync = '??' if analysis_data.get('lip_sync_suitable') else ''
        
        # Get motion data
        motion_speed = analysis_data.get('motion_speed', '?')
        motion_direction = analysis_data.get('motion_direction', '?')
        motion_type = analysis_data.get('motion_type', '?')
        motion_story = analysis_data.get('motion_story', '?')
        best_beats = analysis_data.get('best_beat_types', [])
        editing_style = analysis_data.get('best_editing_style', '?')
        
        print(f'  ? {sync} {subject} | {style} | Energy: {energy}/10')
        print(f'     Motion: speed={motion_speed}/10, dir={motion_direction}, type={motion_type}')
        print(f'     Story: "{motion_story}"')
        print(f'     Best for: {", ".join(best_beats)} | Style: {editing_style}')
        print(f'[ANALYZED] {os.path.basename(video_path)} -> {subject} | {style} | Energy: {energy}/10')

    def _update_smart_bins(self):
        print(f"🚨 _update_smart_bins CALLED! Data count: {len(self.analysis_data)}")
        counts = {k: 0 for k in self.bin_labels.keys()}
        counts['Show All'] = len(self.analysis_data)
        
        for data in self.analysis_data.values():
            s = data.get('subject_type', '').lower()
            style = data.get('art_style', '').lower()
            gender = (data.get('gender') or '').lower()
            energy = data.get('energy_level', 5)
            colors = ' '.join([c.lower() for c in data.get('dominant_colors', [])])
            
            if any(x in s for x in ['person', 'people', 'human']): counts['People'] += 1
            if 'nature' in s: counts['Nature'] += 1
            if 'urban' in s: counts['Urban'] += 1
            if 'object' in s: counts['Objects'] += 1
            
            if any(x in style for x in ['photo', 'realistic']): counts['Photorealistic'] += 1
            if any(x in style for x in ['cgi', '3d', 'render']): counts['CGI/3D'] += 1
            if data.get('is_ai_generated'): counts['AI Generated'] += 1
            
            if 'male' in gender and 'female' not in gender: counts['Male'] += 1
            if 'female' in gender: counts['Female'] += 1
            
            if energy >= 7: counts['High Energy'] += 1
            elif energy >= 4: counts['Medium Energy'] += 1
            else: counts['Low Energy'] += 1
            
            if any(c in colors for c in ['red', 'orange', 'yellow']): counts['Warm Colors'] += 1
            if any(c in colors for c in ['blue', 'green', 'purple']): counts['Cool Colors'] += 1
            
            if data.get('lip_sync_suitable'): counts['Lip Sync Ready'] += 1
        
        for name, count in counts.items():
            text = self.bin_labels[name].text()
            base = text.rsplit('(', 1)[0]
            self.bin_labels[name].setText(f'{base}({count})')

    def _filter_media_bin(self, bin_name):
        for path, item in self.video_files.items():
            if bin_name == 'Show All':
                item.setHidden(False)
            else:
                data = self.analysis_data.get(path, {})
                item.setHidden(not self._match(bin_name, data))

    def _match(self, bin_name, data):
        s = data.get('subject_type', '').lower()
        style = data.get('art_style', '').lower()
        gender = (data.get('gender') or '').lower()
        energy = data.get('energy_level', 5)
        colors = ' '.join([c.lower() for c in data.get('dominant_colors', [])])
        
        return {
            'People': any(x in s for x in ['person', 'people', 'human']),
            'Nature': 'nature' in s,
            'Urban': 'urban' in s,
            'Objects': 'object' in s,
            'Photorealistic': any(x in style for x in ['photo', 'realistic']),
            'CGI/3D': any(x in style for x in ['cgi', '3d', 'render']),
            'AI Generated': data.get('is_ai_generated', False),
            'Male': 'male' in gender and 'female' not in gender,
            'Female': 'female' in gender,
            'High Energy': energy >= 7,
            'Medium Energy': 4 <= energy < 7,
            'Low Energy': energy < 4,
            'Warm Colors': any(c in colors for c in ['red', 'orange', 'yellow']),
            'Cool Colors': any(c in colors for c in ['blue', 'green', 'purple']),
            'Lip Sync Ready': data.get('lip_sync_suitable', False),
        }.get(bin_name, False)

    def reanalyze_all_videos(self):
        for path in list(self.video_files.keys()):
            self.start_analysis(path)

    def get_video_data(self):
        return self.analysis_data








