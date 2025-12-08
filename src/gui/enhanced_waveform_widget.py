"""
BEATSYNC PRO - ENHANCED WAVEFORM VISUALIZER
Cinema-grade audio waveform visualization with neon styling
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QLinearGradient, QBrush
import numpy as np

try:
    from .cinema_colors import CinemaColors as Colors
except ImportError:
    # Fallback colors if cinema_colors not available
    class Colors:
        BG_DEEPEST = "#000000"
        BG_DEEP = "#0F1419"
        NEON_CYAN = "#00D9FF"
        NEON_PURPLE = "#9D4EDD"
        TEXT_TERTIARY = "#8A95A0"


class EnhancedWaveformWidget(QWidget):
    """
    Professional waveform visualization with cinema styling
    Features:
    - Neon cyan/purple gradient waveform
    - RMS energy visualization
    - Beat markers
    - Smooth anti-aliased rendering
    - Deep space background
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(80)
        self.setMaximumHeight(120)
        
        # Waveform data
        self.waveform_data = None
        self.beat_positions = []
        self.current_position = 0.0
        self.duration = 0.0
        
        # Visualization settings
        self.show_beats = True
        self.show_rms = True
        self.style = "neon"  # "neon", "minimal", "bars"
        
        # Animation
        self.animation_offset = 0
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._animate)
        
        # Styling
        self.setStyleSheet(f"background: {Colors.BG_DEEP}; border-radius: 8px;")
    
    def set_waveform_data(self, audio_data, sample_rate=22050):
        """
        Set audio data for waveform visualization
        
        Args:
            audio_data: numpy array of audio samples
            sample_rate: Audio sample rate (default: 22050)
        """
        if audio_data is None or len(audio_data) == 0:
            self.waveform_data = None
            self.update()
            return
        
        # Downsample for display efficiency
        target_samples = self.width() * 2  # 2 samples per pixel
        if len(audio_data) > target_samples:
            step = len(audio_data) // target_samples
            audio_data = audio_data[::step]
        
        # Normalize to -1 to 1 range
        if audio_data.max() > 0:
            audio_data = audio_data / np.abs(audio_data).max()
        
        self.waveform_data = audio_data
        self.duration = len(audio_data) / sample_rate
        self.update()
    
    def set_beat_positions(self, beat_times):
        """
        Set beat marker positions
        
        Args:
            beat_times: List of beat timestamps in seconds
        """
        self.beat_positions = beat_times
        self.update()
    
    def set_position(self, position):
        """
        Set current playback position
        
        Args:
            position: Current position in seconds
        """
        self.current_position = position
        self.update()
    
    def start_animation(self):
        """Start waveform animation"""
        self.animation_timer.start(50)  # 20 FPS
    
    def stop_animation(self):
        """Stop waveform animation"""
        self.animation_timer.stop()
    
    def _animate(self):
        """Animation tick"""
        self.animation_offset = (self.animation_offset + 1) % 100
        self.update()
    
    def paintEvent(self, event):
        """Paint the waveform"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Draw background
        painter.fillRect(0, 0, width, height, QColor(Colors.BG_DEEP))
        
        if self.waveform_data is None or len(self.waveform_data) == 0:
            self._draw_placeholder(painter, width, height)
            return
        
        # Draw based on style
        if self.style == "neon":
            self._draw_neon_waveform(painter, width, height)
        elif self.style == "bars":
            self._draw_bar_waveform(painter, width, height)
        else:
            self._draw_minimal_waveform(painter, width, height)
        
        # Draw beat markers
        if self.show_beats and len(self.beat_positions) > 0:
            self._draw_beat_markers(painter, width, height)
        
        # Draw playhead
        if self.duration > 0:
            self._draw_playhead(painter, width, height)
    
    def _draw_neon_waveform(self, painter, width, height):
        """Draw neon-styled waveform with gradient"""
        center_y = height // 2
        samples = len(self.waveform_data)
        
        # Create gradient brush
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0.0, QColor(Colors.NEON_CYAN))
        gradient.setColorAt(0.5, QColor(Colors.NEON_PURPLE))
        gradient.setColorAt(1.0, QColor(Colors.NEON_CYAN))
        
        # Draw waveform with glow effect
        pen = QPen(QBrush(gradient), 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        points = []
        for i in range(width):
            sample_idx = int((i / width) * samples)
            if sample_idx < samples:
                amplitude = self.waveform_data[sample_idx]
                y = center_y - int(amplitude * (height // 2 - 10))
                points.append((i, y))
        
        # Draw connected line
        if len(points) > 1:
            for i in range(len(points) - 1):
                painter.drawLine(points[i][0], points[i][1], 
                               points[i+1][0], points[i+1][1])
        
        # Draw glow effect (second pass with transparency)
        painter.setOpacity(0.3)
        pen.setWidth(6)
        painter.setPen(pen)
        if len(points) > 1:
            for i in range(len(points) - 1):
                painter.drawLine(points[i][0], points[i][1], 
                               points[i+1][0], points[i+1][1])
        painter.setOpacity(1.0)
    
    def _draw_bar_waveform(self, painter, width, height):
        """Draw bar-style waveform (like audio editors)"""
        center_y = height // 2
        samples = len(self.waveform_data)
        bar_width = 2
        bar_spacing = 1
        bars_per_width = width // (bar_width + bar_spacing)
        
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0.0, QColor(Colors.NEON_CYAN))
        gradient.setColorAt(1.0, QColor(Colors.NEON_PURPLE))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        
        for i in range(bars_per_width):
            sample_idx = int((i / bars_per_width) * samples)
            if sample_idx < samples:
                amplitude = abs(self.waveform_data[sample_idx])
                bar_height = int(amplitude * (height // 2 - 5))
                
                x = i * (bar_width + bar_spacing)
                y_top = center_y - bar_height
                y_bottom = center_y
                
                painter.drawRect(x, y_top, bar_width, bar_height * 2)
    
    def _draw_minimal_waveform(self, painter, width, height):
        """Draw minimal clean waveform"""
        center_y = height // 2
        samples = len(self.waveform_data)
        
        pen = QPen(QColor(Colors.NEON_CYAN), 1)
        painter.setPen(pen)
        
        for i in range(width - 1):
            sample_idx1 = int((i / width) * samples)
            sample_idx2 = int(((i + 1) / width) * samples)
            
            if sample_idx1 < samples and sample_idx2 < samples:
                y1 = center_y - int(self.waveform_data[sample_idx1] * (height // 2 - 5))
                y2 = center_y - int(self.waveform_data[sample_idx2] * (height // 2 - 5))
                painter.drawLine(i, y1, i + 1, y2)
    
    def _draw_beat_markers(self, painter, width, height):
        """Draw vertical lines for beat positions"""
        if self.duration <= 0:
            return
        
        pen = QPen(QColor(Colors.NEON_CYAN), 1)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.setOpacity(0.5)
        
        for beat_time in self.beat_positions:
            x = int((beat_time / self.duration) * width)
            if 0 <= x < width:
                painter.drawLine(x, 0, x, height)
        
        painter.setOpacity(1.0)
    
    def _draw_playhead(self, painter, width, height):
        """Draw current playback position"""
        if self.duration <= 0:
            return
        
        x = int((self.current_position / self.duration) * width)
        
        # Draw playhead line
        pen = QPen(QColor(Colors.NEON_CYAN), 2)
        painter.setPen(pen)
        painter.drawLine(x, 0, x, height)
        
        # Draw glow
        painter.setOpacity(0.3)
        pen.setWidth(6)
        painter.setPen(pen)
        painter.drawLine(x, 0, x, height)
        painter.setOpacity(1.0)
    
    def _draw_placeholder(self, painter, width, height):
        """Draw placeholder when no audio loaded"""
        painter.setPen(QColor(Colors.TEXT_TERTIARY))
        painter.drawText(
            QRect(0, 0, width, height),
            Qt.AlignmentFlag.AlignCenter,
            "No audio loaded"
        )
    
    def resizeEvent(self, event):
        """Handle resize to regenerate waveform"""
        super().resizeEvent(event)
        if self.waveform_data is not None:
            # Trigger redraw on resize
            self.update()


class CompactWaveformWidget(QWidget):
    """
    Compact waveform for audio cards (smaller height)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        
        self.waveform_data = None
        self.setStyleSheet(f"background: transparent;")
    
    def set_waveform_data(self, audio_data):
        """Set audio data"""
        if audio_data is None or len(audio_data) == 0:
            self.waveform_data = None
            self.update()
            return
        
        # Downsample
        target_samples = self.width()
        if len(audio_data) > target_samples:
            step = len(audio_data) // target_samples
            audio_data = audio_data[::step]
        
        # Normalize
        if audio_data.max() > 0:
            audio_data = audio_data / np.abs(audio_data).max()
        
        self.waveform_data = audio_data
        self.update()
    
    def paintEvent(self, event):
        """Paint compact waveform"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_y = height // 2
        
        if self.waveform_data is None or len(self.waveform_data) == 0:
            return
        
        # Draw as bars
        samples = len(self.waveform_data)
        bar_width = max(1, width // samples)
        
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0.0, QColor(Colors.NEON_CYAN))
        gradient.setColorAt(1.0, QColor(Colors.NEON_PURPLE))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setOpacity(0.6)
        
        for i in range(min(samples, width)):
            if i < samples:
                amplitude = abs(self.waveform_data[i])
                bar_height = int(amplitude * (height // 2 - 2))
                
                x = i * bar_width
                y = center_y - bar_height // 2
                
                painter.drawRect(x, y, bar_width, bar_height)


# Convenience function to generate waveform from audio file
def generate_waveform_from_file(audio_path):
    """
    Generate waveform data from audio file using librosa
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        tuple: (waveform_data, sample_rate) or (None, None) on error
    """
    try:
        import librosa
        
        # Load audio (mono, resampled to 22050 Hz)
        y, sr = librosa.load(audio_path, sr=22050, mono=True)
        
        return y, sr
        
    except ImportError:
        print("❌ librosa not installed. Install with: pip install librosa")
        return None, None
    except Exception as e:
        print(f"❌ Error loading audio: {str(e)}")
        return None, None


def generate_beat_positions(audio_path):
    """
    Generate beat positions from audio file
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        list: Beat timestamps in seconds, or empty list on error
    """
    try:
        import librosa
        
        # Load audio
        y, sr = librosa.load(audio_path, sr=22050, mono=True)
        
        # Detect beats
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        return beat_times.tolist()
        
    except ImportError:
        print("❌ librosa not installed")
        return []
    except Exception as e:
        print(f"❌ Error detecting beats: {str(e)}")
        return []
