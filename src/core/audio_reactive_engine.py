"""
BeatSync PRO - Audio Reactive Effects Engine
Real-time effects synchronized to bass, mid, high frequencies
This creates IMPOSSIBLE human coordination
"""

import numpy as np
import librosa
from typing import Dict, List, Tuple
import threading


class AudioReactiveEngine:
    """Generates audio-reactive effects for superhuman sync"""
    
    def __init__(self):
        self.cache = {}
        self.cache_lock = threading.Lock()
    
    def analyze_for_effects(self, audio_path: str, music_structure: Dict) -> Dict:
        """
        Analyze audio for frame-by-frame reactive effects
        
        Returns:
        {
            'bass_hits': [12.045, 12.672, 13.299, ...],  # Exact bass hit times
            'snare_hits': [12.231, 13.458, ...],          # Snare/clap times
            'hihat_pattern': [12.1, 12.2, 12.3, ...],     # Hi-hat rhythm
            'zoom_events': [
                {'time': 12.045, 'strength': 0.8, 'duration': 0.1},  # Zoom pulse
                {'time': 24.1, 'strength': 1.0, 'duration': 0.15}     # Drop zoom
            ],
            'flash_events': [
                {'time': 12.231, 'intensity': 0.6, 'duration': 0.05},
            ],
            'speed_variations': [
                {'start': 60.0, 'end': 75.0, 'start_speed': 1.0, 'end_speed': 1.5},  # Buildup ramp
                {'start': 75.0, 'end': 75.5, 'start_speed': 1.5, 'end_speed': 0.5},  # Drop slow-mo
            ]
        }
        """
        
        cache_key = audio_path
        with self.cache_lock:
            if cache_key in self.cache:
                return self.cache[cache_key]
        
        try:
            print("  🎛️ Audio Reactive Effects Analysis...")
            
            # Load audio
            y, sr = librosa.load(audio_path, sr=22050)
            
            # 1. DETECT BASS HITS (kick drums)
            print("     🥁 Detecting bass hits...")
            bass_hits = self._detect_bass_hits(y, sr)
            
            # 2. DETECT SNARE/CLAP HITS
            print("     👏 Detecting snare hits...")
            snare_hits = self._detect_snare_hits(y, sr)
            
            # 3. DETECT HI-HAT PATTERN
            print("     🎵 Detecting hi-hat pattern...")
            hihat_pattern = self._detect_hihat_pattern(y, sr)
            
            # 4. GENERATE ZOOM EVENTS (bass-reactive)
            print("     🔍 Generating zoom events...")
            zoom_events = self._generate_zoom_events(bass_hits, music_structure)
            
            # 5. GENERATE FLASH EVENTS (snare-reactive)
            print("     ⚡ Generating flash events...")
            flash_events = self._generate_flash_events(snare_hits, music_structure)
            
            # 6. GENERATE SPEED VARIATIONS (build/drop reactive)
            print("     ⚡ Generating speed variations...")
            speed_variations = self._generate_speed_variations(music_structure)
            
            result = {
                'bass_hits': bass_hits,
                'snare_hits': snare_hits,
                'hihat_pattern': hihat_pattern,
                'zoom_events': zoom_events,
                'flash_events': flash_events,
                'speed_variations': speed_variations
            }
            
            with self.cache_lock:
                self.cache[cache_key] = result
            
            print(f"  ✅ Audio Reactive Analysis Complete!")
            print(f"     Bass hits: {len(bass_hits)}")
            print(f"     Snare hits: {len(snare_hits)}")
            print(f"     Zoom events: {len(zoom_events)}")
            print(f"     Flash events: {len(flash_events)}")
            print(f"     Speed variations: {len(speed_variations)}")
            
            return result
            
        except Exception as e:
            print(f"  ❌ Audio reactive analysis error: {e}")
            return self._get_default_reactive_data()
    
    def _detect_bass_hits(self, y: np.ndarray, sr: int) -> List[float]:
        """Detect bass/kick drum hits with millisecond precision"""
        try:
            # Focus on low frequencies (20-200 Hz)
            # Use onset detection on bass-filtered audio
            y_bass = librosa.effects.preemphasis(y, coef=-0.97)  # Boost bass
            
            # Detect onsets (percussive events)
            onset_frames = librosa.onset.onset_detect(
                y=y_bass, 
                sr=sr, 
                hop_length=512,
                backtrack=True,
                units='frames'
            )
            
            # Convert to times
            onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=512)
            
            # Filter for bass-heavy onsets
            bass_hits = []
            hop_length = 512
            
            for onset_time in onset_times:
                frame = librosa.time_to_frames(onset_time, sr=sr, hop_length=hop_length)
                
                # Get frequency content around this onset
                start_frame = max(0, frame - 5)
                end_frame = min(len(y) // hop_length, frame + 5)
                
                # Check if bass-heavy
                if self._is_bass_heavy(y, sr, onset_time):
                    bass_hits.append(round(float(onset_time), 3))
            
            return bass_hits
            
        except Exception as e:
            print(f"       Bass detection error: {e}")
            return []
    
    def _is_bass_heavy(self, y: np.ndarray, sr: int, time: float) -> bool:
        """Check if a moment is bass-heavy"""
        try:
            # Get small window around time
            start = int(time * sr)
            end = min(len(y), start + sr // 10)  # 0.1s window
            
            if end <= start:
                return False
            
            window = y[start:end]
            
            # FFT to analyze frequency content
            fft = np.abs(np.fft.rfft(window))
            freqs = np.fft.rfftfreq(len(window), 1/sr)
            
            # Bass range: 20-200 Hz
            bass_mask = (freqs >= 20) & (freqs <= 200)
            mid_mask = (freqs > 200) & (freqs <= 2000)
            
            bass_energy = np.sum(fft[bass_mask])
            mid_energy = np.sum(fft[mid_mask])
            
            # Bass-heavy if bass > 40% of total
            return bass_energy > (bass_energy + mid_energy) * 0.4
            
        except:
            return False
    
    def _detect_snare_hits(self, y: np.ndarray, sr: int) -> List[float]:
        """Detect snare/clap hits"""
        try:
            # Snares are in mid-high frequencies
            onset_frames = librosa.onset.onset_detect(
                y=y,
                sr=sr,
                hop_length=512,
                units='frames'
            )
            
            onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=512)
            
            snare_hits = []
            for onset_time in onset_times:
                # Check if mid-frequency dominant (snare characteristic)
                if self._is_snare_like(y, sr, onset_time):
                    snare_hits.append(round(float(onset_time), 3))
            
            return snare_hits
            
        except Exception as e:
            print(f"       Snare detection error: {e}")
            return []
    
    def _is_snare_like(self, y: np.ndarray, sr: int, time: float) -> bool:
        """Check if a moment sounds like a snare"""
        try:
            start = int(time * sr)
            end = min(len(y), start + sr // 20)  # 0.05s window
            
            if end <= start:
                return False
            
            window = y[start:end]
            fft = np.abs(np.fft.rfft(window))
            freqs = np.fft.rfftfreq(len(window), 1/sr)
            
            # Snare range: 200-4000 Hz
            snare_mask = (freqs >= 200) & (freqs <= 4000)
            snare_energy = np.sum(fft[snare_mask])
            total_energy = np.sum(fft)
            
            # Snare-like if mid frequencies dominant
            return snare_energy > total_energy * 0.5
            
        except:
            return False
    
    def _detect_hihat_pattern(self, y: np.ndarray, sr: int) -> List[float]:
        """Detect hi-hat/cymbal rhythm"""
        try:
            # Hi-hats are high frequency
            y_high = librosa.effects.preemphasis(y, coef=0.97)  # Boost highs
            
            onset_frames = librosa.onset.onset_detect(
                y=y_high,
                sr=sr,
                hop_length=256,
                units='frames'
            )
            
            onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=256)
            
            # Filter for very short, high-frequency events
            hihat_hits = []
            for t in onset_times:
                if self._is_hihat_like(y, sr, t):
                    hihat_hits.append(round(float(t), 3))
            
            return hihat_hits
            
        except:
            return []
    
    def _is_hihat_like(self, y: np.ndarray, sr: int, time: float) -> bool:
        """Check if sounds like hi-hat"""
        try:
            start = int(time * sr)
            end = min(len(y), start + sr // 40)  # Very short window
            
            if end <= start:
                return False
            
            window = y[start:end]
            fft = np.abs(np.fft.rfft(window))
            freqs = np.fft.rfftfreq(len(window), 1/sr)
            
            # Hi-hat range: 4000+ Hz
            high_mask = freqs >= 4000
            high_energy = np.sum(fft[high_mask])
            total_energy = np.sum(fft)
            
            return high_energy > total_energy * 0.3
            
        except:
            return False
    
    def _generate_zoom_events(self, bass_hits: List[float], music_structure: Dict) -> List[Dict]:
        """Generate zoom pulses synchronized to bass"""
        zoom_events = []
        
        for bass_time in bass_hits:
            # Check energy level at this time
            time_idx = int(bass_time * 10)  # 0.1s resolution
            energy = 0.5
            
            if music_structure and time_idx < len(music_structure.get('energy_curve', [])):
                energy = music_structure['energy_curve'][time_idx]
            
            # Stronger zooms for higher energy
            strength = 0.1 + (energy * 0.2)  # 0.1-0.3 zoom
            
            # Drops get massive zooms
            is_drop = False
            if music_structure and 'drops' in music_structure:
                for drop in music_structure['drops']:
                    if abs(bass_time - drop) < 0.5:  # Within 0.5s of drop
                        strength = 0.5  # MASSIVE zoom
                        is_drop = True
                        break
            
            zoom_events.append({
                'time': bass_time,
                'strength': round(strength, 2),
                'duration': 0.15 if is_drop else 0.1,
                'type': 'drop' if is_drop else 'bass'
            })
        
        return zoom_events
    
    def _generate_flash_events(self, snare_hits: List[float], music_structure: Dict) -> List[Dict]:
        """Generate flash effects on snares"""
        flash_events = []
        
        for snare_time in snare_hits:
            # Quick brightness flash
            flash_events.append({
                'time': snare_time,
                'intensity': 0.3,  # 30% brightness increase
                'duration': 0.05    # Very quick flash
            })
        
        return flash_events
    
    def _generate_speed_variations(self, music_structure: Dict) -> List[Dict]:
        """Generate speed ramps for builds/drops"""
        speed_variations = []
        
        if not music_structure:
            return speed_variations
        
        # Speed up during buildups
        for buildup_start, buildup_end in music_structure.get('buildups', []):
            speed_variations.append({
                'start': buildup_start,
                'end': buildup_end,
                'start_speed': 1.0,
                'end_speed': 1.5,  # 50% faster at peak
                'type': 'buildup'
            })
        
        # Slow-mo at drops
        for drop in music_structure.get('drops', []):
            speed_variations.append({
                'start': drop,
                'end': drop + 0.5,  # 0.5s slow-mo
                'start_speed': 1.5,  # Coming from buildup
                'end_speed': 0.5,    # Dramatic slow-mo
                'type': 'drop_slowmo'
            })
            
            # Recovery after drop
            speed_variations.append({
                'start': drop + 0.5,
                'end': drop + 1.5,
                'start_speed': 0.5,
                'end_speed': 1.0,
                'type': 'drop_recovery'
            })
        
        return speed_variations
    
    def _get_default_reactive_data(self) -> Dict:
        """Fallback data"""
        return {
            'bass_hits': [],
            'snare_hits': [],
            'hihat_pattern': [],
            'zoom_events': [],
            'flash_events': [],
            'speed_variations': []
        }


# Global instance
audio_reactive_engine = AudioReactiveEngine()
