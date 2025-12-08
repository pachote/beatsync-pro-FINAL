"""
BeatSync PRO - Simple Face Detector using OpenCV
NO MEDIAPIPE - No DLL errors!
"""

import cv2
import os
import logging

logger = logging.getLogger(__name__)

class FaceDetector:
    """Simple face detection using OpenCV Haar Cascades - works on Windows!"""
    
    def __init__(self):
        # Use OpenCV's built-in face cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        logger.info("FaceDetector initialized (OpenCV)")
        print("Face Detector initialized (OpenCV - no MediaPipe needed)")
    
    def detect_faces_in_video(self, video_path: str, sample_frames: int = 5) -> dict:
        """Check if video contains faces by sampling frames"""
        if not os.path.exists(video_path):
            return {'has_face': False, 'confidence': 0}
        
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {'has_face': False, 'confidence': 0}
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames < 1:
                cap.release()
                return {'has_face': False, 'confidence': 0}
            
            # Sample frames evenly throughout video
            frame_indices = [int(i * total_frames / (sample_frames + 1)) for i in range(1, sample_frames + 1)]
            
            faces_found = 0
            frames_checked = 0
            
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    continue
                
                frames_checked += 1
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
                
                if len(faces) > 0:
                    faces_found += 1
            
            cap.release()
            
            # If faces found in majority of sampled frames, it's a face clip
            confidence = faces_found / max(frames_checked, 1)
            has_face = confidence >= 0.4  # At least 40% of frames have faces
            
            return {
                'has_face': has_face,
                'confidence': confidence,
                'frames_with_faces': faces_found,
                'frames_checked': frames_checked
            }
            
        except Exception as e:
            logger.warning(f"Face detection error: {e}")
            return {'has_face': False, 'confidence': 0}
