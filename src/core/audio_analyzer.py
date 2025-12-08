"""
BeatSync PRO v15 - Phase 3: ADVANCED AUDIO INTELLIGENCE
Understands instruments, emotions, vocals, frequency content
"""

import librosa
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class AudioAnalyzer:
    def __init__(self):
        self.sample_rate = 22050
        
    def analyze_music(self, audio_path: str) -> Dict:
        """Complete audio analysis with musical intelligence"""
        print(f"\n🎵 PHASE 3: Advanced Audio Intelligence")
        print(f"   Analyzing: {audio_path}")
        
        # Load audio
        y, sr = librosa.load(audio_path, sr=self.sample_rate)
        
        # Basic analysis (existing)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # PHASE 3: Advanced Musical Intelligence
        print("   🎸 Detecting instruments...")
        instruments = self._detect_instruments(y, sr)
        
        print("   😊 Analyzing emotional tone...")
        emotions = self._analyze_emotions(y, sr)
        
        print("   🎤 Detecting vocal presence...")
        vocals = self._detect_vocals(y, sr)
        
        print("   📊 Analyzing frequency content...")
        frequencies = self._analyze_frequencies(y, sr)
        
        print("   ⚡ Computing energy curve...")
        energy_curve = self._compute_energy_curve(y, sr, len(beat_times))
        
        print("   🎼 Analyzing musical sections...")
        sections = self._identify_sections(y, sr, beat_times, energy_curve)
        
        analysis = {
            'bpm': tempo,
            'beats': beat_times.tolist(),
            'duration': duration,
            'instruments': instruments,
            'emotions': emotions,
            'vocals': vocals,
            'frequencies': frequencies,
            'energy_curve': energy_curve,
            'sections': sections
        }
        
        self._print_musical_summary(analysis)
        
        return analysis
    
    def _detect_instruments(self, y: np.ndarray, sr: int) -> Dict:
        """Detect presence and prominence of different instruments"""
        
        # Spectral analysis
        S = np.abs(librosa.stft(y))
        
        # Frequency ranges for instrument detection
        # Bass/Drums: 20-250 Hz
        # Guitar/Keys: 250-2000 Hz  
        # Vocals/High: 2000-8000 Hz
        # Cymbals/Air: 8000+ Hz
        
        freqs = librosa.fft_frequencies(sr=sr)
        
        bass_mask = (freqs >= 20) & (freqs < 250)
        mid_mask = (freqs >= 250) & (freqs < 2000)
        high_mask = (freqs >= 2000) & (freqs < 8000)
        air_mask = freqs >= 8000
        
        bass_energy = np.mean(S[bass_mask, :])
        mid_energy = np.mean(S[mid_mask, :])
        high_energy = np.mean(S[high_mask, :])
        air_energy = np.mean(S[air_mask, :])
        
        total_energy = bass_energy + mid_energy + high_energy + air_energy
        
        instruments = {
            'bass_drums': {
                'presence': float(bass_energy / total_energy),
                'prominence': 'high' if bass_energy > mid_energy else 'medium'
            },
            'guitars_keys': {
                'presence': float(mid_energy / total_energy),
                'prominence': 'high' if mid_energy > bass_energy else 'medium'
            },
            'vocals_leads': {
                'presence': float(high_energy / total_energy),
                'prominence': 'high' if high_energy > mid_energy else 'medium'
            },
            'cymbals_air': {
                'presence': float(air_energy / total_energy),
                'prominence': 'high' if air_energy > 0.1 * total_energy else 'low'
            }
        }
        
        return instruments
    
    def _analyze_emotions(self, y: np.ndarray, sr: int) -> Dict:
        """Analyze emotional characteristics of the music"""
        
        # Tempo-based emotion
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # Spectral features for emotion
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        
        # Mode estimation (major/minor approximation)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        
        # Major tends to have stronger 0, 4, 7 (C, E, G)
        # Minor tends to have stronger 0, 3, 7 (C, Eb, G)
        major_score = chroma_mean[0] + chroma_mean[4] + chroma_mean[7]
        minor_score = chroma_mean[0] + chroma_mean[3] + chroma_mean[7]
        
        mode = 'major' if major_score > minor_score else 'minor'
        
        # Emotional classification
        if tempo > 140 and spectral_centroid > 2000:
            emotion = 'energetic'
            valence = 0.8
        elif tempo > 120 and mode == 'major':
            emotion = 'happy'
            valence = 0.7
        elif tempo < 80 and mode == 'minor':
            emotion = 'melancholic'
            valence = 0.3
        elif tempo > 130 and spectral_centroid > 2500:
            emotion = 'aggressive'
            valence = 0.6
        elif tempo < 90:
            emotion = 'calm'
            valence = 0.5
        else:
            emotion = 'neutral'
            valence = 0.5
        
        return {
            'primary_emotion': emotion,
            'valence': valence,  # 0-1 (sad to happy)
            'energy': float(tempo / 200),  # Normalized energy
            'mode': mode,
            'tension': float(spectral_rolloff / 10000)  # Brightness/tension
        }
    
    def _detect_vocals(self, y: np.ndarray, sr: int) -> Dict:
        """Detect presence and timing of vocals"""
        
        # Harmonic-percussive separation
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        
        # Vocals typically in harmonic component with specific frequency range
        S_harmonic = np.abs(librosa.stft(y_harmonic))
        
        # Vocal frequency range (roughly 200-3000 Hz)
        freqs = librosa.fft_frequencies(sr=sr)
        vocal_mask = (freqs >= 200) & (freqs < 3000)
        
        vocal_energy = np.mean(S_harmonic[vocal_mask, :], axis=0)
        
        # Normalize
        if np.max(vocal_energy) > 0:
            vocal_energy = vocal_energy / np.max(vocal_energy)
        
        # Detect vocal sections (sustained energy above threshold)
        threshold = 0.4
        vocal_presence = vocal_energy > threshold
        
        # Get time positions
        times = librosa.frames_to_time(np.arange(len(vocal_energy)), sr=sr)
        
        # Find vocal sections
        vocal_sections = []
        in_vocal = False
        start_time = 0
        
        for i, present in enumerate(vocal_presence):
            if present and not in_vocal:
                start_time = times[i]
                in_vocal = True
            elif not present and in_vocal:
                vocal_sections.append((start_time, times[i-1]))
                in_vocal = False
        
        if in_vocal:
            vocal_sections.append((start_time, times[-1]))
        
        return {
            'has_vocals': len(vocal_sections) > 0,
            'vocal_percentage': float(np.sum(vocal_presence) / len(vocal_presence)),
            'vocal_sections': vocal_sections,
            'primarily_vocal': float(np.sum(vocal_presence) / len(vocal_presence)) > 0.5,
            'primarily_instrumental': float(np.sum(vocal_presence) / len(vocal_presence)) < 0.3
        }
    
    def _analyze_frequencies(self, y: np.ndarray, sr: int) -> Dict:
        """Analyze frequency content and identify key moments"""
        
        S = np.abs(librosa.stft(y))
        
        # Bass energy over time
        freqs = librosa.fft_frequencies(sr=sr)
        bass_mask = (freqs >= 20) & (freqs < 150)
        bass_energy = np.mean(S[bass_mask, :], axis=0)
        
        # Find bass drops (sudden increases in bass energy)
        bass_diff = np.diff(bass_energy)
        bass_drop_threshold = np.percentile(bass_diff, 95)
        bass_drops = np.where(bass_diff > bass_drop_threshold)[0]
        
        # Convert to time
        bass_drop_times = librosa.frames_to_time(bass_drops, sr=sr)
        
        # High frequency energy (brightness)
        high_mask = freqs >= 4000
        high_energy = np.mean(S[high_mask, :], axis=0)
        
        return {
            'bass_drops': bass_drop_times.tolist(),
            'bass_prominence': float(np.mean(bass_energy)),
            'brightness': float(np.mean(high_energy)),
            'frequency_balance': 'bass_heavy' if np.mean(bass_energy) > np.mean(high_energy) * 2 else 'balanced'
        }
    
    def _compute_energy_curve(self, y: np.ndarray, sr: int, num_beats: int) -> List[float]:
        """Compute energy level at each beat for dynamic pacing"""
        
        # RMS energy
        rms = librosa.feature.rms(y=y)[0]
        
        # Spectral flux (rate of change in spectrum)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        
        # Combine for comprehensive energy measure
        energy = rms * 0.5 + (onset_env / np.max(onset_env)) * 0.5
        
        # Resample to match beat count
        energy_at_beats = np.interp(
            np.linspace(0, len(energy)-1, num_beats),
            np.arange(len(energy)),
            energy
        )
        
        # Normalize to 0-1
        if np.max(energy_at_beats) > 0:
            energy_at_beats = energy_at_beats / np.max(energy_at_beats)
        
        return energy_at_beats.tolist()
    
    def _identify_sections(self, y: np.ndarray, sr: int, beat_times: np.ndarray, 
                          energy_curve: List[float]) -> List[Dict]:
        """Identify musical sections (intro, verse, chorus, etc.)"""
        
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Simple heuristic-based section detection
        sections = []
        
        # Intro (first 20s or 15% of song)
        intro_end = min(20, duration * 0.15)
        sections.append({
            'name': 'intro',
            'start': 0,
            'end': intro_end,
            'energy': 'low',
            'description': 'Opening, establishing mood'
        })
        
        # Body sections based on energy
        body_start = intro_end
        outro_start = duration * 0.85
        
        # Divide body into verse/chorus/bridge based on energy patterns
        body_duration = outro_start - body_start
        
        if body_duration > 60:
            # Longer song - more sections
            sections.append({
                'name': 'verse',
                'start': body_start,
                'end': body_start + body_duration * 0.3,
                'energy': 'medium',
                'description': 'Storytelling section'
            })
            sections.append({
                'name': 'build-up',
                'start': body_start + body_duration * 0.3,
                'end': body_start + body_duration * 0.4,
                'energy': 'rising',
                'description': 'Building tension'
            })
            sections.append({
                'name': 'chorus',
                'start': body_start + body_duration * 0.4,
                'end': body_start + body_duration * 0.7,
                'energy': 'high',
                'description': 'High energy peak'
            })
            sections.append({
                'name': 'bridge',
                'start': body_start + body_duration * 0.7,
                'end': outro_start,
                'energy': 'medium',
                'description': 'Contrast and variety'
            })
        else:
            # Shorter song - simpler structure
            mid_point = body_start + body_duration * 0.5
            sections.append({
                'name': 'verse',
                'start': body_start,
                'end': mid_point,
                'energy': 'medium',
                'description': 'First half'
            })
            sections.append({
                'name': 'chorus',
                'start': mid_point,
                'end': outro_start,
                'energy': 'high',
                'description': 'Second half climax'
            })
        
        # Outro
        sections.append({
            'name': 'outro',
            'start': outro_start,
            'end': duration,
            'energy': 'decreasing',
            'description': 'Resolution and wind down'
        })
        
        return sections
    
    def _print_musical_summary(self, analysis: Dict):
        """Print human-readable summary of musical analysis"""
        print("\n" + "="*60)
        print("🎼 MUSICAL INTELLIGENCE SUMMARY")
        print("="*60)
        
        # Instruments
        inst = analysis['instruments']
        print("\n🎸 INSTRUMENTS:")
        for name, data in inst.items():
            presence_pct = data['presence'] * 100
            print(f"   {name}: {presence_pct:.1f}% ({data['prominence']} prominence)")
        
        # Emotions
        emo = analysis['emotions']
        print(f"\n😊 EMOTION: {emo['primary_emotion']}")
        print(f"   Valence: {emo['valence']:.2f} | Energy: {emo['energy']:.2f}")
        print(f"   Mode: {emo['mode']} | Tension: {emo['tension']:.2f}")
        
        # Vocals
        vox = analysis['vocals']
        print(f"\n🎤 VOCALS: {'Present' if vox['has_vocals'] else 'Instrumental'}")
        print(f"   Coverage: {vox['vocal_percentage']*100:.1f}%")
        if vox['vocal_sections']:
            print(f"   Sections: {len(vox['vocal_sections'])} vocal parts")
        
        # Frequencies
        freq = analysis['frequencies']
        print(f"\n📊 FREQUENCIES:")
        print(f"   Bass drops: {len(freq['bass_drops'])} detected")
        print(f"   Balance: {freq['frequency_balance']}")
        
        # Sections
        print(f"\n🎼 SECTIONS:")
        for sec in analysis['sections']:
            print(f"   {sec['start']:.1f}-{sec['end']:.1f}s: {sec['name']} ({sec['energy']} energy)")
        
        print("="*60 + "\n")
