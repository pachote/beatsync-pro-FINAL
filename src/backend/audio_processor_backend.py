import os
import numpy as np
from pathlib import Path
from pydub import AudioSegment
import librosa
import psutil
from PySide6.QtCore import QThread, Signal

class AudioCache:
    def __init__(self, cache_dir="cache/audio"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_index = {}

class AudioProcessorBackend:
    def __init__(self):
        self.cache = AudioCache()
        self.current_audio = None
        self.current_audio_data = None
        self.current_sample_rate = None
        self.current_duration = 0
    
    def load_audio(self, filepath):
        print(f"Loading: {filepath}")
        audio = AudioSegment.from_file(filepath)
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / 32768.0
        self.current_audio_data = samples
        self.current_sample_rate = audio.frame_rate
        self.current_duration = len(audio) / 1000.0
        return {
            "audio_data": samples,
            "sample_rate": audio.frame_rate,
            "duration": len(audio) / 1000.0
        }

class BeatDetectionThread(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished_analysis = Signal(dict)
    error = Signal(str)
    
    def __init__(self, audio_data, sample_rate):
        super().__init__()
        self.audio_data = audio_data
        self.sample_rate = sample_rate
    
    def run(self):
        try:
            self.progress.emit(20)
            tempo, beats = librosa.beat.beat_track(
                y=self.audio_data,
                sr=self.sample_rate,
                units="time"
            )
            if isinstance(tempo, np.ndarray):
                tempo = float(tempo[0])
            self.progress.emit(100)
            analysis = {
                "bpm": round(tempo, 1),
                "beats": beats.tolist() if hasattr(beats, "tolist") else beats,
                "downbeats": [],
                "duration": len(self.audio_data) / self.sample_rate
            }
            self.finished_analysis.emit(analysis)
        except Exception as e:
            self.error.emit(str(e))

class MemoryManager:
    def __init__(self):
        pass
    
    def get_memory_usage(self):
        process = psutil.Process()
        return {"rss_mb": process.memory_info().rss / (1024 * 1024)}
    
    def check_memory(self):
        return "OK"

print("Audio backend loaded!")
