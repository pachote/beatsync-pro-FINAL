"""
BeatSync Pro - Beat Detector
Audio beat detection and analysis using librosa
"""

import os
import json
import numpy as np

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    print("Warning: librosa not installed. Using fallback beat detection.")
    LIBROSA_AVAILABLE = False


class BeatDetector:
    """Main beat detection class using librosa"""
    
    def __init__(self):
        self.sample_rate = None
        self.audio_data = None
        
    def analyze_audio(self, file_path):
        """Analyze audio file and return beat information"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        if not LIBROSA_AVAILABLE:
            # Return basic fallback data
            return self._fallback_analysis(file_path)
        
        try:
            # Load audio file
            audio_data, sr = librosa.load(file_path, sr=None, mono=True)
            self.audio_data = audio_data
            self.sample_rate = sr
            
            # Beat tracking
            tempo, beats = librosa.beat.beat_track(
                y=audio_data, 
                sr=sr, 
                units='time',
                trim=False
            )
            
            # Handle numpy array tempo
            if isinstance(tempo, np.ndarray):
                tempo = float(tempo[0]) if len(tempo) > 0 else float(tempo)
            else:
                tempo = float(tempo)
            
            # Onset detection
            onset_frames = librosa.onset.onset_detect(
                y=audio_data,
                sr=sr,
                backtrack=True
            )
            onsets = librosa.frames_to_time(onset_frames, sr=sr)
            
            # Key detection (simplified)
            chroma = librosa.feature.chroma_cqt(y=audio_data, sr=sr)
            key = self._estimate_key(chroma)
            
            # Duration
            duration = len(audio_data) / sr
            
            # Build analysis result
            analysis = {
                'tempo': tempo,
                'beats': beats.tolist() if isinstance(beats, np.ndarray) else list(beats),
                'onsets': onsets.tolist() if isinstance(onsets, np.ndarray) else list(onsets),
                'key': key,
                'genre': 'unknown',
                'duration': duration,
                'sample_rate': sr,
                'sections': [],
                'vocal_sections': [],
                'confidence': 85.0,
                'source_file': file_path,
                'audio_data': audio_data,
                'sr': sr
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return self._fallback_analysis(file_path)
    
    def _estimate_key(self, chroma):
        """Estimate musical key from chroma features"""
        # Simplified key detection
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        if chroma is not None and len(chroma) > 0:
            key_index = np.argmax(np.sum(chroma, axis=1))
            return keys[key_index]
        return 'C'
    
    def _fallback_analysis(self, file_path):
        """Fallback analysis when librosa is not available"""
        # Return minimal valid data structure
        return {
            'tempo': 120.0,
            'beats': [i * 0.5 for i in range(100)],  # Fake beats every 0.5 seconds
            'onsets': [i * 0.5 for i in range(100)],
            'key': 'C',
            'genre': 'unknown',
            'duration': 50.0,
            'sample_rate': 44100,
            'sections': [],
            'vocal_sections': [],
            'confidence': 10.0,
            'source_file': file_path,
            'audio_data': np.zeros(44100 * 50),  # 50 seconds of silence
            'sr': 44100
        }