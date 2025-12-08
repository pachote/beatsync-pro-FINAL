"""
BeatSync Pro - Music Tab
Handles audio selection, beat analysis, and waveform display
"""
import os
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLabel, QProgressBar, QGroupBox,
    QGridLayout, QSplitter, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, Signal, QThread, QFileInfo

# Add parent directories to path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from src.gui.widgets.audio_visualizers import AudioVisualizerPanel
except ImportError:
    AudioVisualizerPanel = None

from src.core.cache_manager import CacheManager

class BeatAnalysisThread(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished_analysis = Signal(dict)
    error = Signal(str)

    def __init__(self, audio_path, cache_manager):
        super().__init__()
        self.audio_path = audio_path
        self.cache_manager = cache_manager

    def run(self):
        try:
            self.status.emit("Checking cache...")
            self.progress.emit(10)

            cached_data = self.cache_manager.load_analysis(self.audio_path)
            if cached_data:
                cached_data['source_file_path'] = self.audio_path
                self.status.emit("Loaded from cache")
                self.progress.emit(100)
                self.finished_analysis.emit(cached_data)
                return

            import librosa
            import numpy as np

            self.status.emit("Loading audio...")
            self.progress.emit(20)
            y, sr = librosa.load(self.audio_path, sr=None, mono=True)
            duration = librosa.get_duration(y=y, sr=sr)

            self.status.emit("Analyzing beat track...")
            self.progress.emit(40)
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            beats = librosa.frames_to_time(beat_frames, sr=sr)

            if isinstance(tempo, np.ndarray):
                tempo = float(tempo.item())
            else:
                tempo = float(tempo)

            self.status.emit("Analyzing key...")
            self.progress.emit(80)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            key_corr = np.corrcoef(chroma, librosa.key_to_chroma('C:maj'))
            key = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][np.argmax(key_corr[0, 1:])]

            analysis = {
                'tempo': tempo,
                'beats': beats.tolist(),
                'key': key,
                'duration': duration,
                'source_file_path': self.audio_path
            }

            self.status.emit("Saving to cache...")
            self.progress.emit(90)
            
            # Create a copy for caching without the full file path
            cache_payload = analysis.copy()
            cache_payload.pop('source_file_path', None)
            self.cache_manager.save_analysis(self.audio_path, cache_payload)

            self.status.emit("Analysis complete!")
            self.progress.emit(100)
            self.finished_analysis.emit(analysis)

        except Exception as e:
            self.error.emit(f"Analysis error: {str(e)}")
            self.progress.emit(0)

class MusicTab(QWidget):
    analysis_complete = Signal(dict)

    def __init__(self, cache_manager, parent=None):
        super().__init__(parent)
        self.cache_manager = cache_manager
        self.audio_files = []
        self.current_audio = None
        self.analysis_thread = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Vertical)
        
        # Create and add sections
        top_controls = self.create_controls_section()
        self.visualizer_panel = self.create_visualizer_section()
        self.info_panel = self.create_info_section()

        layout.addWidget(top_controls)
        splitter.addWidget(self.visualizer_panel)
        splitter.addWidget(self.info_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

    def create_controls_section(self):
        container = QGroupBox("Audio Controls")
        layout = QHBoxLayout()
        
        self.import_audio_btn = QPushButton("Import Audio")
        self.import_audio_btn.clicked.connect(self.import_audio_files)
        layout.addWidget(self.import_audio_btn)
        
        self.audio_selector = QComboBox()
        self.audio_selector.setMinimumWidth(250)
        self.audio_selector.currentTextChanged.connect(self.on_audio_selected)
        layout.addWidget(QLabel("Current Audio:"))
        layout.addWidget(self.audio_selector)

        self.analyze_btn = QPushButton("Analyze Beat")
        self.analyze_btn.clicked.connect(self.analyze_current_audio)
        self.analyze_btn.setEnabled(False)
        layout.addWidget(self.analyze_btn)

        self.clear_cache_btn = QPushButton("Clear Cache")
        self.clear_cache_btn.clicked.connect(self.clear_cache)
        layout.addWidget(self.clear_cache_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        container.setLayout(layout)
        return container

    def create_visualizer_section(self):
        if AudioVisualizerPanel:
            return AudioVisualizerPanel()
        else:
            placeholder = QLabel("AudioVisualizerPanel module not found.")
            placeholder.setAlignment(Qt.AlignCenter)
            return placeholder

    def create_info_section(self):
        container = QGroupBox("Analysis Results")
        layout = QGridLayout()
        self.info_labels = {
            'BPM': QLabel("--"), 'Key': QLabel("--"),
            'Beats': QLabel("--"), 'Duration': QLabel("--")
        }
        layout.addWidget(QLabel("<b>BPM:</b>"), 0, 0)
        layout.addWidget(self.info_labels['BPM'], 0, 1)
        layout.addWidget(QLabel("<b>Key:</b>"), 0, 2)
        layout.addWidget(self.info_labels['Key'], 0, 3)
        layout.addWidget(QLabel("<b>Beats:</b>"), 1, 0)
        layout.addWidget(self.info_labels['Beats'], 1, 1)
        layout.addWidget(QLabel("<b>Duration:</b>"), 1, 2)
        layout.addWidget(self.info_labels['Duration'], 1, 3)
        container.setLayout(layout)
        return container
    
    def import_audio_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Import Audio", "", "Audio Files (*.mp3 *.wav *.m4a *.flac)")
        if files:
            for file_path in files:
                if not any(f[1] == file_path for f in self.audio_files):
                    file_info = QFileInfo(file_path)
                    self.audio_files.append((file_info.lastModified(), file_path))
            
            # Sort by newest first
            self.audio_files.sort(key=lambda x: x[0], reverse=True)
            self.update_audio_list()

    def update_audio_list(self):
        self.audio_selector.clear()
        for _, file_path in self.audio_files:
            self.audio_selector.addItem(os.path.basename(file_path), file_path)
        if self.audio_files:
            self.audio_selector.setCurrentIndex(0)

    def on_audio_selected(self, text):
        if not text:
            self.current_audio = None
            self.analyze_btn.setEnabled(False)
            self.display_analysis(None)
            if AudioVisualizerPanel: self.visualizer_panel.clear()
            return
        
        self.current_audio = self.audio_selector.currentData()
        self.analyze_btn.setEnabled(True)
        cached = self.cache_manager.load_analysis(self.current_audio)
        if cached:
            self.status_label.setText("Cached analysis found.")
            cached['source_file_path'] = self.current_audio
            self.on_analysis_complete(cached)
        else:
            self.status_label.setText("Ready to analyze.")
            self.display_analysis(None)
            if AudioVisualizerPanel: self.visualizer_panel.clear()
            
    def analyze_current_audio(self):
        if not self.current_audio: return
        self.analyze_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.analysis_thread = BeatAnalysisThread(self.current_audio, self.cache_manager)
        self.analysis_thread.progress.connect(self.progress_bar.setValue)
        self.analysis_thread.status.connect(self.status_label.setText)
        self.analysis_thread.finished_analysis.connect(self.on_analysis_complete)
        self.analysis_thread.error.connect(self.on_analysis_error)
        self.analysis_thread.start()

    def on_analysis_complete(self, analysis):
        self.display_analysis(analysis)
        self.analyze_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Analysis complete!")
        # **CRITICAL FIX**: Pass data to the visualizer
        if AudioVisualizerPanel and hasattr(self.visualizer_panel, 'display_audio_analysis'):
            self.visualizer_panel.display_audio_analysis(analysis)
        self.analysis_complete.emit(analysis)

    def on_analysis_error(self, error_msg):
        QMessageBox.warning(self, "Analysis Error", error_msg)
        self.analyze_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Analysis failed.")

    def display_analysis(self, analysis):
        if not analysis:
            for label in self.info_labels.values():
                label.setText("--")
            return
            
        self.info_labels['BPM'].setText(f"{analysis.get('tempo', 0):.1f}")
        self.info_labels['Key'].setText(analysis.get('key', '--'))
        self.info_labels['Beats'].setText(str(len(analysis.get('beats', []))))
        duration = analysis.get('duration', 0)
        self.info_labels['Duration'].setText(f"{int(duration // 60)}:{int(duration % 60):02d}")

    def clear_cache(self):
        reply = QMessageBox.question(self, "Clear Cache", "Clear all cached analyses?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            count = self.cache_manager.clear_all_cache()
            self.status_label.setText(f"Cleared {count} cache files.")
            # **CRITICAL FIX**: Reset the UI after clearing
            self.display_analysis(None)
            if AudioVisualizerPanel: self.visualizer_panel.clear()
            if self.current_audio: # Re-check the current file to show "Ready to analyze"
                self.on_audio_selected(self.audio_selector.currentText())