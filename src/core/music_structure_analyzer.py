"""
BeatSync PRO - Music Structure Intelligence
Detects vocals, drops, buildups, breakdowns, energy curves
This is what makes editing GENIUS level
"""

import librosa
import numpy as np
from typing import Dict, List, Tuple
import threading


class MusicStructureAnalyzer:
    """Analyzes music at a deep level - understands structure, vocals, energy"""
    
    def __init__(self):
        self.cache = {}
        self.cache_lock = threading.Lock()
    
    def analyze_music_structure(self, audio_path: str) -> Dict:
        """
        Deep music analysis for AGI-level editing
        
        Returns:
        {
            'sections': [
                {'start': 0.0, 'end': 30.0, 'type': 'intro', 'energy': 0.3},
                {'start': 30.0, 'end': 60.0, 'type': 'verse', 'energy': 0.6, 'has_vocals': True},
                {'start': 60.0, 'end': 75.0, 'type': 'buildup', 'energy': 0.8},
                {'start': 75.0, 'end': 90.0, 'type': 'drop', 'energy': 1.0}
            ],
            'vocal_segments': [(30.0, 60.0), (90.0, 120.0)],
            'drops': [75.0, 150.0],
            'buildups': [(60.0, 75.0), (140.0, 150.0)],
            'energy_curve': [0.3, 0.32, 0.35, ...],  # Every 0.1s
            'frequency_bands': {
                'bass': [...],     # Low frequency energy
                'mid': [...],      # Mid frequency energy  
                'high': [...]      # High frequency energy
            }
        }
        """
        
        cache_key = audio_path
        with self.cache_lock:
            if cache_key in self.cache:
                return self.cache[cache_key]
        
        try:
            print("  🎵 Deep Music Analysis Starting...")
            
            # Load audio
            y, sr = librosa.load(audio_path, sr=22050)
            duration = librosa.get_duration(y=y, sr=sr)
            
            print(f"     Duration: {duration:.1f}s | Sample Rate: {sr}Hz")
            
            # 1. ENERGY CURVE (every 0.1s for precise sync)
            print("  📊 Computing energy curve...")
            hop_length = int(sr * 0.1)  # 0.1 second resolution
            rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
            energy_curve = (rms / np.max(rms)).tolist()  # Normalize 0-1
            
            # 2. FREQUENCY BAND ANALYSIS
            print("  🎛️ Analyzing frequency bands...")
            stft = np.abs(librosa.stft(y, hop_length=hop_length))
            
            # Split into bass, mid, high
            bass_end = int(stft.shape[0] * 0.15)    # 0-15% = bass
            mid_end = int(stft.shape[0] * 0.5)      # 15-50% = mid
            
            bass = np.mean(stft[:bass_end, :], axis=0)
            mid = np.mean(stft[bass_end:mid_end, :], axis=0)
            high = np.mean(stft[mid_end:, :], axis=0)
            
            # Normalize
            bass = (bass / np.max(bass)).tolist()
            mid = (mid / np.max(mid)).tolist()
            high = (high / np.max(high)).tolist()
            
            # 3. VOCAL DETECTION
            print("  🎤 Detecting vocals...")
            vocal_segments = self._detect_vocals(y, sr, duration)
            
            # 4. DROP DETECTION (sudden energy spikes)
            print("  💥 Detecting drops...")
            drops = self._detect_drops(energy_curve, duration)
            
            # 5. BUILDUP DETECTION (increasing energy)
            print("  📈 Detecting buildups...")
            buildups = self._detect_buildups(energy_curve, duration)
            
            # 6. SECTION CLASSIFICATION
            print("  🎼 Classifying sections...")
            sections = self._classify_sections(energy_curve, vocal_segments, drops, buildups, duration)
            
            result = {
                'duration': duration,
                'energy_curve': energy_curve,
                'frequency_bands': {
                    'bass': bass,
                    'mid': mid,
                    'high': high
                },
                'vocal_segments': vocal_segments,
                'drops': drops,
                'buildups': buildups,
                'sections': sections
            }
            
            with self.cache_lock:
                self.cache[cache_key] = result
            
            print(f"  ✅ Music Intelligence Complete!")
            print(f"     Sections: {len(sections)}")
            print(f"     Vocals: {len(vocal_segments)} segments")
            print(f"     Drops: {len(drops)}")
            print(f"     Buildups: {len(buildups)}")
            
            return result
            
        except Exception as e:
            print(f"  ❌ Music analysis error: {e}")
            return self._get_default_music_data(audio_path)
    
    def _detect_vocals(self, y: np.ndarray, sr: int, duration: float) -> List[Tuple[float, float]]:
        """Detect vocal segments using harmonic/percussive separation"""
        try:
            # Separate harmonics (vocals/melody) from percussive (drums)
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            
            # Get RMS of harmonic component
            hop_length = sr // 10  # 0.1s resolution
            rms_harmonic = librosa.feature.rms(y=y_harmonic, hop_length=hop_length)[0]
            rms_percussive = librosa.feature.rms(y=y_percussive, hop_length=hop_length)[0]
            
            # Vocals = where harmonic is dominant
            harmonic_ratio = rms_harmonic / (rms_percussive + 1e-8)
            
            # Threshold for vocal presence
            vocal_threshold = np.percentile(harmonic_ratio, 60)
            is_vocal = harmonic_ratio > vocal_threshold
            
            # Convert to time segments
            times = librosa.frames_to_time(np.arange(len(is_vocal)), sr=sr, hop_length=hop_length)
            
            vocal_segments = []
            in_vocal = False
            start = 0
            
            for i, (vocal, t) in enumerate(zip(is_vocal, times)):
                if vocal and not in_vocal:
                    start = t
                    in_vocal = True
                elif not vocal and in_vocal:
                    if t - start > 2.0:  # Minimum 2s vocal segment
                        vocal_segments.append((round(start, 1), round(t, 1)))
                    in_vocal = False
            
            # Close last segment
            if in_vocal and duration - start > 2.0:
                vocal_segments.append((round(start, 1), round(duration, 1)))
            
            return vocal_segments
            
        except Exception as e:
            print(f"     Vocal detection error: {e}")
            return []
    
    def _detect_drops(self, energy_curve: List[float], duration: float) -> List[float]:
        """Detect drops (sudden massive energy spikes)"""
        drops = []
        
        for i in range(5, len(energy_curve) - 1):
            # Look for sudden jump
            avg_before = np.mean(energy_curve[i-5:i])
            current = energy_curve[i]
            
            # Drop = 50%+ energy increase from average
            if current > avg_before * 1.5 and current > 0.7:
                time = i * 0.1  # Convert index to seconds
                
                # Avoid duplicates (drops within 10s)
                if not drops or time - drops[-1] > 10.0:
                    drops.append(round(time, 1))
        
        return drops
    
    def _detect_buildups(self, energy_curve: List[float], duration: float) -> List[Tuple[float, float]]:
        """Detect buildups (sustained energy increase)"""
        buildups = []
        
        window = 30  # 3 second window
        
        for i in range(window, len(energy_curve) - 5):
            # Check if energy is consistently increasing
            window_data = energy_curve[i-window:i]
            
            if len(window_data) < window:
                continue
            
            # Linear regression to detect upward trend
            x = np.arange(len(window_data))
            slope = np.polyfit(x, window_data, 1)[0]
            
            # Buildup = positive slope above threshold
            if slope > 0.01:  # Significant increase
                start_time = (i - window) * 0.1
                end_time = i * 0.1
                
                # Avoid duplicates
                if not buildups or start_time - buildups[-1][1] > 5.0:
                    buildups.append((round(start_time, 1), round(end_time, 1)))
        
        return buildups
    
    def _classify_sections(self, energy_curve: List[float], vocal_segments: List, 
                          drops: List[float], buildups: List, duration: float) -> List[Dict]:
        """Classify music into sections"""
        sections = []
        
        # Simple classification based on energy levels
        section_length = 15.0  # 15 second sections
        num_sections = int(duration / section_length) + 1
        
        for i in range(num_sections):
            start = i * section_length
            end = min((i + 1) * section_length, duration)
            
            # Get average energy for this section
            start_idx = int(start * 10)
            end_idx = int(end * 10)
            section_energy = np.mean(energy_curve[start_idx:end_idx]) if end_idx > start_idx else 0.5
            
            # Check if has vocals
            has_vocals = any(v_start <= start < v_end or v_start <= end < v_end 
                           for v_start, v_end in vocal_segments)
            
            # Check if has drop
            has_drop = any(start <= d < end for d in drops)
            
            # Check if has buildup
            has_buildup = any(start <= b_start < end for b_start, b_end in buildups)
            
            # Classify section type
            if i == 0:
                section_type = 'intro'
            elif end >= duration - 15:
                section_type = 'outro'
            elif has_drop:
                section_type = 'drop'
            elif has_buildup:
                section_type = 'buildup'
            elif has_vocals:
                section_type = 'verse' if section_energy < 0.7 else 'chorus'
            elif section_energy < 0.4:
                section_type = 'breakdown'
            else:
                section_type = 'section'
            
            sections.append({
                'start': round(start, 1),
                'end': round(end, 1),
                'type': section_type,
                'energy': round(section_energy, 2),
                'has_vocals': has_vocals,
                'has_drop': has_drop,
                'has_buildup': has_buildup
            })
        
        return sections
    
    def _get_default_music_data(self, audio_path: str) -> Dict:
        """Fallback if analysis fails"""
        try:
            y, sr = librosa.load(audio_path, sr=22050)
            duration = librosa.get_duration(y=y, sr=sr)
        except:
            duration = 180.0
        
        return {
            'duration': duration,
            'energy_curve': [0.5] * int(duration * 10),
            'frequency_bands': {
                'bass': [0.5] * int(duration * 10),
                'mid': [0.5] * int(duration * 10),
                'high': [0.5] * int(duration * 10)
            },
            'vocal_segments': [],
            'drops': [],
            'buildups': [],
            'sections': [{'start': 0, 'end': duration, 'type': 'section', 'energy': 0.5, 'has_vocals': False}]
        }


# Global instance
music_structure_analyzer = MusicStructureAnalyzer()
