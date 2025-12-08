"""Centralized cache management - fixes all cache issues"""
import os
import json
from pathlib import Path

class CacheManager:
    def __init__(self):
        # Path is '.../src/core' -> go up three levels to 'RENDEREELSTUDIO_BEATSYNC' and into 'data'
        self.cache_dir = Path(__file__).parent.parent.parent / 'data'
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_path(self, audio_file):
        """Get cache file path for audio file"""
        basename = os.path.basename(audio_file)
        name_only = os.path.splitext(basename)[0]
        # Cache Format: [filename]_beats.json
        return self.cache_dir / f"{name_only}_beats.json"
    
    def get_analysis(self, audio_file):
        """Check if cache exists and load analysis from cache if exists."""
        return self.load_analysis(audio_file)

    def save_analysis(self, audio_file, analysis):
        """Save analysis to cache - FIXED to handle dictionary input"""
        cache_path = self.get_cache_path(audio_file)
        
        # FIX: Handle analysis as dictionary (not object with attributes)
        if isinstance(analysis, dict):
            # Already a dictionary, just ensure proper types
            data = {
                'tempo': float(analysis.get('tempo', 0.0)),
                'beats': analysis.get('beats', []),
                'onsets': analysis.get('onsets', []),
                'key': analysis.get('key', 'Unknown'),
                'genre': analysis.get('genre', 'unknown'),
                'duration': float(analysis.get('duration', 0.0)),
                'sample_rate': int(analysis.get('sample_rate', 44100)),
                'source_file': os.path.basename(audio_file),
                'confidence': float(analysis.get('confidence', 0.0))
            }
        else:
            # Handle as object with attributes (legacy support)
            data = {
                'tempo': float(analysis.tempo) if hasattr(analysis, 'tempo') else 0.0,
                'beats': analysis.beats.tolist() if hasattr(analysis, 'beats') else [],
                'onsets': analysis.onsets.tolist() if hasattr(analysis, 'onsets') else [],
                'key': analysis.key if hasattr(analysis, 'key') else 'Unknown',
                'genre': analysis.genre if hasattr(analysis, 'genre') else 'unknown',
                'duration': analysis.duration if hasattr(analysis, 'duration') else 0.0,
                'sample_rate': analysis.sample_rate if hasattr(analysis, 'sample_rate') else 44100,
                'source_file': os.path.basename(audio_file),
                'confidence': analysis.confidence if hasattr(analysis, 'confidence') else 0.0
            }
        
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ [CacheManager] Saved cache to {cache_path}")
        return cache_path
    
    def load_analysis(self, audio_file):
        """Load analysis from cache if exists"""
        cache_path = self.get_cache_path(audio_file)
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                print(f"✅ [CacheManager] Loaded cache from {cache_path}")
                return data
            except (json.JSONDecodeError, IOError) as e:
                print(f"❌ [CacheManager] Error loading cache {cache_path}: {e}")
                # Delete corrupted cache file
                try:
                    cache_path.unlink()
                except:
                    pass
                return None
        return None
    
    def has_cache(self, audio_file):
        """Check if cache exists for file"""
        cache_path = self.get_cache_path(audio_file)
        return cache_path.exists()
    
    def clear_cache_for_file(self, audio_file):
        """Clear cache for specific file"""
        cache_path = self.get_cache_path(audio_file)
        if cache_path.exists():
            try:
                cache_path.unlink()
                print(f"✅ [CacheManager] Deleted cache: {cache_path}")
                return True
            except OSError as e:
                print(f"❌ [CacheManager] Error deleting {cache_path}: {e}")
        return False
    
    def clear_all_cache(self):
        """Clear ALL cache files - ENHANCED with better error handling"""
        cleared = 0
        failed = 0
        
        # Get list of all cache files
        cache_files = list(self.cache_dir.glob('*_beats.json'))
        total = len(cache_files)
        
        for cache_file in cache_files:
            try:
                cache_file.unlink()
                cleared += 1
                print(f"✅ [CacheManager] Deleted: {cache_file.name}")
            except OSError as e:
                failed += 1
                print(f"❌ [CacheManager] Error deleting {cache_file}: {e}")
        
        print(f"✅ [CacheManager] Cache clear complete: {cleared}/{total} files deleted, {failed} failed")
        return cleared
    
    def list_cached_files(self):
        """List all cached files"""
        cached = []
        for cache_file in self.cache_dir.glob('*_beats.json'):
            cached.append(cache_file.stem.replace('_beats', ''))
        return cached
    
    def get_cache_size(self):
        """Get total size of all cache files in bytes"""
        total_size = 0
        for cache_file in self.cache_dir.glob('*_beats.json'):
            total_size += cache_file.stat().st_size
        return total_size