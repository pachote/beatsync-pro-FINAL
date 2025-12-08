import cv2
from PySide6.QtCore import QThread, Signal, QSize
from PySide6.QtGui import QImage, QPixmap, QIcon

class ThumbnailWorker(QThread):
    finished = Signal(str, QIcon)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                return

            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Get frame from 10% into the video
            frame_to_capture = int(frame_count * 0.1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_to_capture)
            
            ret, frame = cap.read()
            cap.release()

            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                icon = QIcon(pixmap)
                self.finished.emit(self.video_path, icon)
        except Exception as e:
            print(f"Thumbnail generation failed for {self.video_path}: {e}")
