import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, QRect
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QLinearGradient, QPainterPath, QFont

class WaveformWidget(QWidget):
    position_changed = Signal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.audio_data = None
        self.sample_rate = 44100
        self.duration = 0
        self.beat_times = []
        self.current_position = 0
        self.bg_color = QColor(30, 32, 35)
        self.waveform_color_top = QColor(0, 200, 255)
        self.waveform_color_bottom = QColor(147, 0, 211)
        self.beat_color = QColor(255, 255, 255, 120)
        self.playhead_color = QColor(255, 255, 255)
        self.setMinimumHeight(150)
        self.setMouseTracking(True)

    def load_audio(self, file_path):
        try:
            import librosa
            self.audio_data, self.sample_rate = librosa.load(file_path, sr=None, mono=True)
            self.duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)
            self.update()
        except Exception as e:
            print(f"Error loading audio for waveform: {e}")

    def set_beat_markers(self, beat_times):
        self.beat_times = beat_times
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self.bg_color)
        
        if self.audio_data is None:
            painter.setPen(QPen(QColor(100, 100, 120)))
            painter.setFont(QFont("Arial", 11))
            painter.drawText(self.rect(), Qt.AlignCenter, "Import a music file to see the waveform")
            return

        width = self.width()
        height = self.height()
        mid_y = height // 2
        
        # Downsample for performance
        num_samples = len(self.audio_data)
        samples_per_pixel = num_samples // width
        if samples_per_pixel < 1: samples_per_pixel = 1

        path_top = QPainterPath()
        path_bottom = QPainterPath()
        path_top.moveTo(0, mid_y)
        path_bottom.moveTo(0, mid_y)

        for i in range(width):
            start = i * samples_per_pixel
            end = start + samples_per_pixel
            chunk = self.audio_data[start:end]
            if len(chunk) > 0:
                max_val = np.max(chunk)
                min_val = np.min(chunk)
            else:
                max_val, min_val = 0, 0
            
            path_top.lineTo(i, mid_y - (max_val * mid_y * 0.9))
            path_bottom.lineTo(i, mid_y - (min_val * mid_y * 0.9))

        # Create gradient for waveform
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0.0, self.waveform_color_top)
        gradient.setColorAt(1.0, self.waveform_color_bottom)
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(gradient))

        # Clip the painter to draw the top and bottom paths correctly
        full_path = QPainterPath()
        full_path.addPath(path_top)
        full_path.addPath(path_bottom)
        painter.drawPath(full_path)
        
        # Draw beat markers
        if self.duration > 0:
            painter.setPen(QPen(self.beat_color, 1, Qt.DotLine))
            for beat_time in self.beat_times:
                x = int((beat_time / self.duration) * width)
                painter.drawLine(x, 0, x, height)
