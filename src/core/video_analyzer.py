import torch
from transformers import pipeline, AutoImageProcessor, TimesformerForVideoClassification
from ultralytics import YOLO
import os
import cv2
from PIL import Image
import numpy as np

class AdvancedVideoAnalyzer:
    def __init__(self, model_path='yolov8m.pt'):
        self.is_ready = False
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"Booting Dynamic Reasoning Engine...")
        print(f"Targeting compute device: cuda:{self.device}")

        # --- AI MODEL 1: Zero-Shot for Scenery/Style (No change) ---
        self.classifier = pipeline("zero-shot-image-classification", model="openai/clip-vit-large-patch14", device=self.device)
        
        # --- AI MODEL 2: YOLO for Objects (No change) ---
        self.yolo_model = YOLO(model_path)
        
        # --- AI MODEL 3: Timesformer for Action Recognition ---
        self.action_processor = AutoImageProcessor.from_pretrained("facebook/timesformer-base-finetuned-k400")
        self.action_model = TimesformerForVideoClassification.from_pretrained("facebook/timesformer-base-finetuned-k400").to(self.device if self.device != -1 else 'cpu')

        print("--- Dynamic Reasoning Engine is Online. ---")
        self.is_ready = True
        self.director = AI_Director()
    
    def _extract_frames(self, video_path, num_frames=8):
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames < num_frames: return []
        
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        frames = []
        for i in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        cap.release()
        return frames

    def analyze_video_content(self, video_path):
        print(f"Performing action analysis on: {os.path.basename(video_path)}...")
        try:
            frames = self._extract_frames(video_path)
            if not frames: return {}
            
            pil_image = frames[len(frames) // 2] # Use middle frame for static analysis

            # --- YOLO Analysis ---
            yolo_frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            yolo_results = self.yolo_model(yolo_frame, verbose=False)
            people, objects = [], []
            if yolo_results[0].boxes:
                names = yolo_results[0].names
                for box in yolo_results[0].boxes:
                    label = names[int(box.cls)]
                    if label == 'person': people.append('person')
                    else: objects.append(label)
            
            # --- Zero-Shot Analysis ---
            candidate_labels = ["cyberpunk city", "nature landscape", "abstract background", "studio lighting", "concert stage", "neon glow", "cinematic", "vibrant colors", "dark mood", "fire and sparks", "particle effects", "light rays"]
            classification_results = self.classifier(pil_image, candidate_labels=candidate_labels)
            scenery = [res['label'] for res in classification_results if res['score'] > 0.9 and any(kw in res['label'] for kw in ["city", "landscape", "background", "stage"])]
            effects = [res['label'] for res in classification_results if res['score'] > 0.9 and not any(kw in res['label'] for kw in ["city", "landscape", "background", "stage"])]

            # --- Action Recognition Analysis ---
            video_pt = self.action_processor(frames, return_tensors="pt").to(self.device if self.device != -1 else 'cpu')
            with torch.no_grad():
                outputs = self.action_model(**video_pt)
                logits = outputs.logits
            
            predicted_class_idx = logits.argmax(-1).item()
            action = [self.action_model.config.id2label[predicted_class_idx]]

            analysis_results = {
                'people': list(set(people)), 'action': action, 'scenery': scenery,
                'objects': list(set(objects)), 'effects': effects
            }
            print(f" -> Found: {analysis_results}")
            return analysis_results

        except Exception as e:
            print(f"Error analyzing {os.path.basename(video_path)}: {e}")
            return {}

class AI_Director:
    def __init__(self): self.THRESHOLDS = {}
    def update_tuning_parameters(self, new_thresholds=None): pass
    def generate_edit_plan(self, creative_prompt, video_data, audio_analysis, generation_rules): return ["Placeholder EDL"]

