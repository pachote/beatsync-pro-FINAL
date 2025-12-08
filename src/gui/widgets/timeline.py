"""
Timeline Widget - Shows ALL clips properly
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

class TimelineWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(140)
        self.video_clips = []
        self.duration = 0
        self.beat_markers = []
        self.video_track = self
        
    def populate_timeline(self, clips, duration, beat_times=None):
        """Populate with ALL clips"""
        try:
            self.video_clips = clips if isinstance(clips, list) else []
            self.duration = max(duration, 1)
            self.beat_markers = beat_times if beat_times else []
            
            print(f"[TIMELINE] ✅ Loaded {len(self.video_clips)} clips, duration {self.duration}s")
            
            # Debug: Show first few clips
            for i, clip in enumerate(self.video_clips[:3]):
                if isinstance(clip, dict):
                    print(f"  Clip {i}: {clip.get('start_time', 0)}s-{clip.get('duration', 0)}s")
            
            self.update()
        except Exception as e:
            print(f"[TIMELINE ERROR] {e}")
        
    def paintEvent(self, event):
        """Paint with ALL clips visible"""
        painter = QPainter(self)
        
        try:
            width = self.width()
            height = self.height()
            
            # Dark background
            painter.fillRect(0, 0, width, height, QColor(20, 20, 20))
            
            video_h = int(height * 0.5)
            audio_h = height - video_h
            
            # === VIDEO TRACK ===
            painter.setPen(QPen(QColor(200, 200, 200)))
            painter.drawText(5, 12, f"📹 Video ({len(self.video_clips)} clips)")
            
            if self.video_clips and self.duration > 0:
                px_per_sec = width / self.duration
                
                # Draw ALL clips
                for i, clip in enumerate(self.video_clips):
                    try:
                        if isinstance(clip, dict):
                            start = clip.get('start_time', 0)
                            dur = clip.get('duration', 5)
                        else:
                            start = i * 5
                            dur = 5
                        
                        x = int(start * px_per_sec)
                        w = max(int(dur * px_per_sec) - 1, 2)
                        
                        # Colorful clips
                        hue = (i * 40) % 360
                        color = QColor.fromHsv(hue, 220, 200)
                        painter.setBrush(QBrush(color))
                        painter.setPen(QPen(QColor(255, 255, 255, 80), 1))
                        painter.drawRect(x, 20, w, video_h - 25)
                        
                    except Exception as e:
                        print(f"[TIMELINE] Error clip {i}: {e}")
                
                # Beat markers
                painter.setPen(QPen(QColor(255, 255, 0, 200), 2))
                for beat in self.beat_markers:
                    bx = int(beat * px_per_sec)
                    if 0 <= bx <= width:
                        painter.drawLine(bx, 18, bx, video_h - 3)
            
            # === AUDIO TRACK ===
            audio_y = video_h
            painter.setPen(QPen(QColor(200, 200, 200)))
            painter.drawText(5, audio_y + 12, "🎵 Audio Waveform")
            
            # Waveform bars
            if self.duration > 0:
                painter.setPen(Qt.NoPen)
                bar_w = 3
                for x in range(0, width, bar_w + 1):
                    import random
                    random.seed(x)
                    h = int((audio_h - 30) * (0.2 + random.random() * 0.8))
                    mid = audio_y + 20 + (audio_h - 30) // 2
                    
                    painter.setBrush(QBrush(QColor(60, 150, 255)))
                    painter.drawRect(x, mid - h//2, bar_w, h)
                
                # Beat markers on audio
                painter.setPen(QPen(QColor(255, 200, 0, 180), 1))
                for beat in self.beat_markers:
                    bx = int(beat * px_per_sec)
                    if 0 <= bx <= width:
                        painter.drawLine(bx, audio_y + 18, bx, height - 3)
            
        except Exception as e:
            print(f"[TIMELINE PAINT ERROR] {e}")
            painter.fillRect(0, 0, width, height, QColor(60, 20, 20))
            painter.setPen(QColor(255, 100, 100))
            painter.drawText(10, 30, f"Error: {str(e)[:40]}")
        
        finally:
            painter.end()
