"""
BeatSync Pro - Audio Visualizers Module
IMPROVED: Renders a professional, gradient-filled symmetrical waveform.
"""
import numpy as np
import os
import librosa
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QPainterPath

class WaveformWidget(QWidget):
    """Internal widget that performs the actual waveform drawing."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.audio_data = None
        self.setMinimumHeight(150)

    def set_audio_data(self, audio_data):
        self.audio_data = audio_data
        self.update()

    def clear(self):
        self.set_audio_data(None)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#1e1e1e"))

        if self.audio_data is None or len(self.audio_data) == 0:
            painter.setPen(QColor("#FF9800"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Waveform visualization will appear here\nAnalyze audio to see the waveform")
            return

        width = self.width()
        height = self.height()
        mid_y = height / 2
        
        samples_per_pixel = len(self.audio_data) // width
        if samples_per_pixel < 1: samples_per_pixel = 1

        # --- NEW DRAWING LOGIC ---
        path_top = QPainterPath()
        path_bottom = QPainterPath()
        path_top.moveTo(0, mid_y)
        path_bottom.moveTo(0, mid_y)

        for x in range(width):
            chunk = self.audio_data[x * samples_per_pixel:(x + 1) * samples_per_pixel]
            if len(chunk) > 0:
                max_val = np.max(chunk)
                path_top.lineTo(x, mid_y - (max_val * mid_y))
                path_bottom.lineTo(x, mid_y - (np.min(chunk) * mid_y)) # Use min for bottom half of top wave
        
        # Create a combined path for filling
        fill_path = QPainterPath(path_top)
        # Create a reversed version of the bottom path to close the shape
        reversed_bottom = QPainterPath()
        for i in range(fill_path.elementCount() -1, -1, -1):
             el = fill_path.elementAt(i)
             reversed_bottom.lineTo(el.x, height - el.y) # Mirror vertically
        fill_path.connectPath(reversed_bottom)
        
        # Gradient Fill
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor(0, 255, 255))   # Cyan
        gradient.setColorAt(0.5, QColor(33, 150, 243)) # Blue
        gradient.setColorAt(1, QColor(148, 0, 211))   # Purple
        
        painter.fillPath(fill_path, QBrush(gradient))

        # Center Line
        painter.setPen(QPen(QColor(255, 255, 255, 50), 1))
        painter.drawLine(0, mid_y, width, mid_y)
        # --- END NEW DRAWING LOGIC ---

class AudioVisualizerPanel(QWidget):
    # This class remains unchanged, it just passes data through
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self); layout.setContentsMargins(0, 0, 0, 0)
        self.waveform_widget = WaveformWidget(); layout.addWidget(self.waveform_widget)
    def display_audio_analysis(self, analysis_data):
        file_path = analysis_data.get("source_file_path")
        if file_path and os.path.exists(file_path):
            try:
                y, sr = librosa.load(file_path, sr=None, mono=True)
                self.waveform_widget.set_audio_data(y)
            except Exception as e:
                print(f"Visualizer Error: {e}"); self.waveform_widget.clear()
        else: self.waveform_widget.clear()
    def clear(self):
        self.waveform_widget.clear()