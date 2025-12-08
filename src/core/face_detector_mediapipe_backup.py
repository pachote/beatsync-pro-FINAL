"""
Face Detector using OpenCV Haar Cascade
Fallback from MediaPipe due to DLL issues
"""
import cv2
import os
from pathlib import Path

class FaceDetector:
    """Detect faces in video clips using OpenCV Haar Cascade"""
    
    def __init__(self):
        self.face_cascade = None
        self.available = False
        
        # Try to load Haar cascade
        try:
            # OpenCV includes this cascade file
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(cascade_path):
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                if not self.face_cascade.empty():
                    self.available = True
                    print("FaceDetector initialized (OpenCV Haar Cascade)")
                else:
                    print("FaceDetector: Cascade file failed to load")
            else:
                print(f"FaceDetector: Cascade file not found at {cascade_path}")
        except Exception as e:
            print(f"FaceDetector init error: {e}")
    
    def detect_faces_in_video(self, video_path: str, sample_frames: int = 5) -> dict:
        """
        Detect if video contains faces
        Returns dict with face detection info
        """
        if not self.available:
            return {"has_face": False, "confidence": 0.0, "face_regions": []}
        
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {"has_face": False, "confidence": 0.0, "face_regions": []}
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames <= 0:
                cap.release()
                return {"has_face": False, "confidence": 0.0, "face_regions": []}
            
            # Sample frames evenly throughout video
            frame_indices = [int(i * total_frames / (sample_frames + 1)) for i in range(1, sample_frames + 1)]
            
            faces_detected = 0
            all_regions = []
            
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    continue
                
                # Convert to grayscale for detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(50, 50)
                )
                
                if len(faces) > 0:
                    faces_detected += 1
                    h, w = frame.shape[:2]
                    for (x, y, fw, fh) in faces:
                        all_regions.append({
                            "x": x / w,
                            "y": y / h,
                            "width": fw / w,
                            "height": fh / h
                        })
            
            cap.release()
            
            confidence = faces_detected / sample_frames
            has_face = confidence >= 0.3  # Face in 30%+ of sampled frames
            
            return {
                "has_face": has_face,
                "confidence": confidence,
                "face_regions": all_regions[:10]  # Limit regions
            }
            
        except Exception as e:
            print(f"Face detection error: {e}")
            return {"has_face": False, "confidence": 0.0, "face_regions": []}
    
    def get_lip_region(self, video_path: str) -> dict:
        """
        Get lip region for a face in video
        Returns approximate lip region based on face detection
        """
        result = self.detect_faces_in_video(video_path, sample_frames=3)
        
        if not result["has_face"] or not result["face_regions"]:
            return None
        
        # Use first detected face region
        face = result["face_regions"][0]
        
        # Estimate lip region (lower third of face)
        lip_region = {
            "x": face["x"] + face["width"] * 0.2,
            "y": face["y"] + face["height"] * 0.65,
            "width": face["width"] * 0.6,
            "height": face["height"] * 0.25
        }
        
        return lip_region


def detect_faces_in_clips(clips: list, detector: FaceDetector = None) -> list:
    """
    Filter clips to find those containing faces
    Returns list of clips with face detection results
    """
    if detector is None:
        detector = FaceDetector()
    
    if not detector.available:
        print("Face detector not available")
        return []
    
    face_clips = []
    
    for clip in clips:
        video_path = clip.get("path") or clip.get("video_path")
        if not video_path:
            continue
        
        result = detector.detect_faces_in_video(video_path)
        
        if result["has_face"]:
            clip_info = clip.copy()
            clip_info["face_detection"] = result
            face_clips.append(clip_info)
    
    return face_clips
