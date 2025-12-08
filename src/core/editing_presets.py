"""
EDITING PRESETS SYSTEM
AGI-level intelligent clip duration and pacing algorithms
"""

class EditingPreset:
    """Defines intelligent editing styles based on music genre and energy"""
    
    PRESETS = {
        'chill': {
            'name': 'Chill',
            'clip_count_range': (30, 40),
            'duration_range': (3.0, 5.0),
            'description': 'Slow, smooth transitions. Ballads, acoustic.',
            'energy_threshold': 0.4,
            'clip_mix': {'short': 0.1, 'medium': 0.3, 'long': 0.6, 'ultra_short': 0.0}
        },
        'balanced': {
            'name': 'Balanced',
            'clip_count_range': (50, 70),
            'duration_range': (2.0, 4.0),
            'description': 'Mix of pacing. Great for most genres.',
            'energy_threshold': 0.6,
            'clip_mix': {'short': 0.4, 'medium': 0.4, 'long': 0.2, 'ultra_short': 0.0}
        },
        'dynamic': {
            'name': 'Dynamic',
            'clip_count_range': (80, 100),
            'duration_range': (1.5, 3.0),
            'description': 'Fast-paced. Ideal for pop and rock.',
            'energy_threshold': 0.75,
            'clip_mix': {'short': 0.5, 'medium': 0.3, 'long': 0.1, 'ultra_short': 0.1}
        },
        'flash_cuts': {
            'name': 'Flash Cuts',
            'clip_count_range': (120, 150),
            'duration_range': (0.5, 1.5),
            'description': 'Rapid cuts on every beat. Electronic.',
            'energy_threshold': 0.85,
            'clip_mix': {'short': 0.6, 'medium': 0.2, 'long': 0.05, 'ultra_short': 0.15}
        },
        'hypercut': {
            'name': 'Hypercut',
            'clip_count_range': (180, 250),
            'duration_range': (0.3, 1.0),
            'description': 'Extreme fast cutting. Experimental.',
            'energy_threshold': 0.95,
            'clip_mix': {'short': 0.3, 'medium': 0.1, 'long': 0.05, 'ultra_short': 0.55}
        }
    }
    
    @classmethod
    def get_preset(cls, preset_name='balanced'):
        """Get preset configuration"""
        return cls.PRESETS.get(preset_name.lower(), cls.PRESETS['balanced'])
    
    @classmethod
    def calculate_clip_duration(cls, preset_name, beat_interval, energy_level):
        """Calculate intelligent clip duration based on music"""
        preset = cls.get_preset(preset_name)
        min_dur, max_dur = preset['duration_range']
        
        # Adjust duration based on energy
        if energy_level > preset['energy_threshold']:
            # High energy = shorter clips
            duration = min_dur + (max_dur - min_dur) * 0.3
        else:
            # Low energy = longer clips
            duration = min_dur + (max_dur - min_dur) * 0.7
        
        # Snap to beat intervals for musical sync
        beats_per_clip = max(1, round(duration / beat_interval))
        final_duration = beats_per_clip * beat_interval
        
        return final_duration
    
    @classmethod
    def get_target_clip_count(cls, preset_name, song_duration):
        """Calculate target number of clips"""
        preset = cls.get_preset(preset_name)
        min_count, max_count = preset['clip_count_range']
        
        # Scale based on song duration
        target = int((min_count + max_count) / 2)
        
        return min(target, max_count)
