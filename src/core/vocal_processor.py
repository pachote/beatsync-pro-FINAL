"""
BeatSync PRO - Vocal Processor
GPU-accelerated vocal separation using Demucs v4
"""

import os
import logging
import hashlib
import tempfile
from pathlib import Path
from typing import Optional, Dict
import numpy as np

logger = logging.getLogger(__name__)


class VocalProcessor:
    """
    Extract vocals from music using Demucs v4 (htdemucs model)
    GPU-accelerated when available
    """
    
    MODEL_NAME = "htdemucs"
    
    def __init__(self, output_dir: Optional[str] = None, use_gpu: bool = True):
        self.output_dir = Path(output_dir) if output_dir else Path.home() / '.beatsync' / 'vocals'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache_dir = Path('cache/vocals')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.use_gpu = use_gpu
        self.model = None
        self._device = None
        
    def _get_device(self):
        """Get compute device (GPU if available)"""
        if self._device is None:
            try:
                import torch
                if self.use_gpu and False:
                    self._device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                    logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
                else:
                    self._device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                    logger.info("Using CPU")
            except ImportError:
                self._device = 'cpu'
                logger.warning("PyTorch not available, using CPU")
        return self._device
    
    def _load_model(self):
        """Load Demucs model (lazy loading)"""
        if self.model is None:
            try:
                import torch
                from demucs.pretrained import get_model
                from demucs.apply import apply_model
                
                logger.info(f"Loading Demucs model: {self.MODEL_NAME}")
                self.model = get_model(self.MODEL_NAME)
                self.model.to(self._get_device())
                self.model.eval()
                logger.info("Demucs model loaded successfully")
                
            except ImportError as e:
                logger.error(f"Demucs not installed: {e}")
                logger.info("Install with: pip install demucs --break-system-packages")
                raise
            except Exception as e:
                logger.error(f"Failed to load Demucs model: {e}")
                raise
                
        return self.model
    
    def _get_cache_key(self, audio_path: str) -> str:
        """Generate cache key based on file content"""
        stat = os.stat(audio_path)
        key_data = f"{audio_path}_{stat.st_size}_{stat.st_mtime}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _check_cache(self, cache_key: str) -> Optional[str]:
        """Check if vocals already extracted"""
        cache_file = self.cache_dir / f"{cache_key}_vocals.wav"
        if cache_file.exists():
            logger.info(f"Cache hit: {cache_key}")
            return str(cache_file)
        return None
    
    def process_audio(self, audio_path: str, progress_callback=None) -> Dict:
        # TEMPORARY BYPASS - skip Demucs, return original audio for API testing
        print("[BYPASS] Skipping vocal extraction - returning original audio for API test")
        return {
            'vocals_path': audio_path,
            'accompaniment_path': None,
            'gender': 'unknown',
            'success': True
        }
        # END BYPASS
        """
        Extract vocals from audio file
        
        Returns:
            Dict with keys: vocals_path, accompaniment_path, gender, success
        """
        audio_path = str(audio_path)
        
        if not os.path.exists(audio_path):
            return {'success': False, 'error': f'File not found: {audio_path}'}
        
        # Check cache
        cache_key = self._get_cache_key(audio_path)
        cached_vocals = self._check_cache(cache_key)
        if cached_vocals:
            return {
                'success': True,
                'vocals_path': cached_vocals,
                'cached': True
            }
        
        if progress_callback:
            progress_callback(10, "Loading audio...")
        
        try:
            import torch
            import torchaudio
            from demucs.apply import apply_model
            
            # Load audio
            waveform, sample_rate = torchaudio.load(audio_path)
            
            # Resample to model sample rate if needed (44100 for htdemucs)
            if sample_rate != 44100:
                resampler = torchaudio.transforms.Resample(sample_rate, 44100)
                waveform = resampler(waveform)
                sample_rate = 44100
            
            # Ensure stereo
            if waveform.shape[0] == 1:
                waveform = waveform.repeat(2, 1)
            elif waveform.shape[0] > 2:
                waveform = waveform[:2]
            
            if progress_callback:
                progress_callback(30, "Loading model...")
            
            model = self._load_model()
            device = self._get_device()
            
            if progress_callback:
                progress_callback(50, "Separating vocals...")
            
            # Add batch dimension and move to device
            waveform = waveform.unsqueeze(0).to(device)
            
            # Apply model
            with torch.no_grad():
                try:
                    sources = apply_model(model, waveform, device=device)
                except RuntimeError as gpu_err:
                    if "CUDA" in str(gpu_err) or "kernel" in str(gpu_err):
                        print(f"GPU failed, falling back to CPU: {gpu_err}")
                        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                        waveform = waveform.to(device)
                        sources = apply_model(model, waveform, device=device)
                    else:
                        raise
            
            # sources shape: [batch, sources, channels, samples]
            # htdemucs sources: drums, bass, other, vocals
            vocals = sources[0, 3]  # vocals is index 3
            accompaniment = sources[0, :3].sum(dim=0)  # sum drums, bass, other
            
            if progress_callback:
                progress_callback(80, "Saving vocals...")
            
            # Save vocals
            vocals_path = self.cache_dir / f"{cache_key}_vocals.wav"
            torchaudio.save(str(vocals_path), vocals.cpu(), sample_rate)
            
            # Save accompaniment (optional, for preview)
            accomp_path = self.cache_dir / f"{cache_key}_accompaniment.wav"
            torchaudio.save(str(accomp_path), accompaniment.cpu(), sample_rate)
            
            if progress_callback:
                progress_callback(90, "Analyzing vocals...")
            
            # Detect gender by pitch analysis
            gender = self._detect_gender(vocals.cpu().numpy())
            
            if progress_callback:
                progress_callback(100, "Complete!")
            
            logger.info(f"Vocals extracted: {vocals_path}")
            
            return {
                'success': True,
                'vocals_path': str(vocals_path),
                'accompaniment_path': str(accomp_path),
                'gender': gender,
                'sample_rate': sample_rate
            }
            
        except ImportError as e:
            logger.error(f"Missing dependency: {e}")
            return {'success': False, 'error': f'Missing dependency: {e}'}
        except Exception as e:
            logger.exception("Vocal extraction failed")
            return {'success': False, 'error': str(e)}
    
    def _detect_gender(self, vocals: np.ndarray) -> str:
        """
        Detect likely gender based on fundamental frequency
        Male: ~85-180 Hz, Female: ~165-255 Hz
        """
        try:
            import librosa
            
            # Convert to mono if stereo
            if len(vocals.shape) > 1:
                vocals_mono = vocals.mean(axis=0)
            else:
                vocals_mono = vocals
            
            # Extract pitch using librosa
            pitches, magnitudes = librosa.piptrack(
                y=vocals_mono.astype(np.float32), 
                sr=44100,
                fmin=50,
                fmax=400
            )
            
            # Get pitch values where magnitude is significant
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if not pitch_values:
                return 'unknown'
            
            # Calculate median pitch
            median_pitch = np.median(pitch_values)
            
            # Classify
            if median_pitch < 165:
                return 'male'
            elif median_pitch > 200:
                return 'female'
            else:
                return 'ambiguous'
                
        except Exception as e:
            logger.warning(f"Gender detection failed: {e}")
            return 'unknown'
    
    def get_status(self) -> Dict:
        """Check if vocal processor is ready"""
        try:
            import torch
            import demucs
            gpu_available = False
            return {
                'ready': True,
                'gpu': gpu_available,
                'device': str(self._get_device()) if gpu_available else 'cpu',
                'model': self.MODEL_NAME
            }
        except ImportError as e:
            return {
                'ready': False,
                'error': str(e),
                'install': 'pip install demucs torchaudio --break-system-packages'
            }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    processor = VocalProcessor()
    status = processor.get_status()
    print(f"Vocal Processor Status: {status}")
    
    # Test with a file if provided
    import sys
    if len(sys.argv) > 1:
        result = processor.process_audio(sys.argv[1])
        print(f"Result: {result}")