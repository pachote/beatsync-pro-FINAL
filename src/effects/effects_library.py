"""
Effects Library - Comprehensive FFmpeg Effect Definitions
Defines all available effects with parameters, compatibility, and constraints
"""

# ========================================
# COLOR GRADING EFFECTS
# ========================================
COLOR_GRADES = {
    'cinematic_teal_orange': {
        'description': 'Hollywood blockbuster look',
        'ffmpeg_filter': 'eq=contrast=1.2:brightness=0.05:saturation=1.1,colorbalance=rs=0.3:bs=-0.2:rm=0.1:bh=-0.05',
        'compatibility': ['film_grain', 'vignette', 'subtle_glow'],
        'intensity_range': (0.5, 0.9),
        'genre_fit': ['cinematic', 'drama', 'action']
    },
    'cyberpunk_neon': {
        'description': 'High contrast neon colors for electronic music',
        'ffmpeg_filter': 'eq=contrast=1.5:saturation=1.4:gamma=1.1',
        'compatibility': ['chromatic_aberration', 'glitch', 'rgb_glow'],
        'intensity_range': (0.6, 1.0),
        'genre_fit': ['electronic', 'edm', 'synthwave']
    },
    'vintage_film': {
        'description': 'Warm nostalgic film look',
        'ffmpeg_filter': 'curves=preset=cross_process,eq=saturation=0.7:brightness=0.05',
        'compatibility': ['film_grain', 'vignette', 'light_leaks'],
        'intensity_range': (0.4, 0.8),
        'genre_fit': ['indie', 'folk', 'vintage']
    },
    'dreamy_ethereal': {
        'description': 'Soft romantic glow',
        'ffmpeg_filter': 'eq=saturation=0.8:brightness=0.1:contrast=0.9',
        'compatibility': ['soft_glow', 'light_leaks', 'subtle_blur'],
        'intensity_range': (0.3, 0.7),
        'genre_fit': ['ballad', 'ambient', 'dream_pop']
    },
    'dark_moody': {
        'description': 'Desaturated dark tones',
        'ffmpeg_filter': 'eq=contrast=1.3:saturation=0.6:brightness=-0.1',
        'compatibility': ['vignette', 'film_grain'],
        'intensity_range': (0.5, 0.9),
        'genre_fit': ['rock', 'metal', 'gothic']
    },
    'vibrant_pop': {
        'description': 'Bright saturated colors',
        'ffmpeg_filter': 'eq=saturation=1.3:brightness=0.05:contrast=1.1',
        'compatibility': ['subtle_glow', 'sharp_details'],
        'intensity_range': (0.6, 0.9),
        'genre_fit': ['pop', 'hip_hop', 'dance']
    }
}

# ========================================
# VISUAL EFFECTS
# ========================================
VISUAL_FX = {
    'film_grain': {
        'description': 'Organic film texture',
        'ffmpeg_filter': 'noise=c0s={intensity}:c0f=t+u',
        'default_params': {'intensity': 20},
        'param_range': {'intensity': (15, 30)},
        'compatibility': ['vignette', 'color_grade', 'vintage_film'],
        'incompatible': ['glitch', 'pixelize']
    },
    'chromatic_aberration': {
        'description': 'RGB channel separation (lens distortion)',
        'ffmpeg_filter': 'rgbashift=rh={rh}:gh={gh}:bh={bh}',
        'default_params': {'rh': 5, 'gh': -5, 'bh': 0},
        'param_range': {'rh': (2, 8), 'gh': (-8, -2), 'bh': (-3, 3)},
        'compatibility': ['glitch', 'cyberpunk_neon', 'rgb_glow'],
        'incompatible': ['soft_glow', 'dreamy_ethereal']
    },
    'vignette': {
        'description': 'Darkened corners for focus',
        'ffmpeg_filter': 'vignette=angle=PI/{angle}',
        'default_params': {'angle': 5},
        'param_range': {'angle': (3, 8)},
        'compatibility': ['film_grain', 'cinematic', 'dark_moody']
    },
    'soft_glow': {
        'description': 'Dreamy highlight bloom',
        'ffmpeg_filter': 'split[main][blur];[blur]boxblur={radius}:1[blurred];[main][blurred]blend=all_mode=lighten:all_opacity={opacity}',
        'default_params': {'radius': 20, 'opacity': 0.5},
        'param_range': {'radius': (10, 30), 'opacity': (0.3, 0.7)},
        'compatibility': ['dreamy_ethereal', 'ballad', 'ambient'],
        'incompatible': ['chromatic_aberration', 'glitch']
    },
    'rgb_glow': {
        'description': 'Neon glow on bright areas',
        'ffmpeg_filter': 'split[main][blur];[blur]boxblur=30[blurred];[main][blurred]blend=all_mode=screen:all_opacity={opacity}',
        'default_params': {'opacity': 0.6},
        'param_range': {'opacity': (0.4, 0.8)},
        'compatibility': ['cyberpunk_neon', 'electronic', 'synthwave']
    },
    'subtle_blur': {
        'description': 'Soft focus effect',
        'ffmpeg_filter': 'gblur=sigma={sigma}',
        'default_params': {'sigma': 0.5},
        'param_range': {'sigma': (0.3, 1.5)},
        'compatibility': ['dreamy_ethereal', 'soft_glow']
    },
    'sharp_details': {
        'description': 'Enhanced clarity',
        'ffmpeg_filter': 'unsharp=5:5:{strength}',
        'default_params': {'strength': 1.2},
        'param_range': {'strength': (0.8, 2.0)},
        'compatibility': ['vibrant_pop', 'action']
    }
}

# ========================================
# TRANSITIONS
# ========================================
TRANSITIONS = {
    'fade': {
        'description': 'Smooth opacity transition',
        'ffmpeg_filter': 'xfade=transition=fade:duration={duration}:offset={offset}',
        'default_duration': 0.5,
        'genre_fit': ['ballad', 'ambient', 'cinematic']
    },
    'dissolve': {
        'description': 'Cross-dissolve blend',
        'ffmpeg_filter': 'xfade=transition=dissolve:duration={duration}:offset={offset}',
        'default_duration': 0.5,
        'genre_fit': ['pop', 'indie', 'folk']
    },
    'circleopen': {
        'description': 'Circular reveal',
        'ffmpeg_filter': 'xfade=transition=circleopen:duration={duration}:offset={offset}',
        'default_duration': 0.8,
        'genre_fit': ['electronic', 'creative']
    },
    'pixelize': {
        'description': 'Pixelated transition',
        'ffmpeg_filter': 'xfade=transition=pixelize:duration={duration}:offset={offset}',
        'default_duration': 0.3,
        'genre_fit': ['electronic', 'glitch', 'hip_hop']
    },
    'wipeleft': {
        'description': 'Left to right wipe',
        'ffmpeg_filter': 'xfade=transition=wipeleft:duration={duration}:offset={offset}',
        'default_duration': 0.4,
        'genre_fit': ['action', 'energetic']
    },
    'cut': {
        'description': 'Direct cut (no transition)',
        'ffmpeg_filter': None,
        'default_duration': 0,
        'genre_fit': ['all']
    }
}

# ========================================
# MOTION EFFECTS
# ========================================
MOTION_FX = {
    'zoom_in_slow': {
        'description': 'Gradual zoom into frame',
        'ffmpeg_filter': "scale=1920:1080,zoompan=z='zoom+0.001':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080",
        'requires_preprocessing': True
    },
    'zoom_in_fast': {
        'description': 'Rapid zoom for impact',
        'ffmpeg_filter': "scale=1920:1080,zoompan=z='zoom+0.003':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080",
        'requires_preprocessing': True
    },
    'speed_ramp_slow': {
        'description': 'Slow motion effect',
        'ffmpeg_filter': 'setpts=2.0*PTS',
        'audio_filter': 'atempo=0.5'
    },
    'speed_ramp_fast': {
        'description': 'Speed up footage',
        'ffmpeg_filter': 'setpts=0.5*PTS',
        'audio_filter': 'atempo=2.0'
    }
}

# ========================================
# BEAT-SYNCHRONIZED EFFECTS
# ========================================
BEAT_FX = {
    'flash': {
        'description': 'Quick brightness flash on beat',
        'ffmpeg_filter': "eq=contrast={intensity}:enable='between(t,{start},{end})'",
        'default_params': {'intensity': 2.0, 'duration': 0.05},
        'genre_fit': ['electronic', 'edm', 'hip_hop']
    },
    'pulse_scale': {
        'description': 'Scale pulse on beat',
        'ffmpeg_filter': "scale='iw*{scale}:ih*{scale}':enable='between(t,{start},{end})'",
        'default_params': {'scale': 1.05, 'duration': 0.1},
        'genre_fit': ['electronic', 'dance']
    },
    'color_shift': {
        'description': 'Quick color shift on beat',
        'ffmpeg_filter': "eq=saturation={sat}:enable='between(t,{start},{end})'",
        'default_params': {'sat': 2.0, 'duration': 0.1},
        'genre_fit': ['electronic', 'psychedelic']
    }
}

# ========================================
# EFFECT COMPATIBILITY MATRIX
# ========================================
COMPATIBILITY_MATRIX = {
    'film_grain': {'vignette': 0.9, 'vintage_film': 0.9, 'cinematic': 0.8, 'glitch': 0.2},
    'chromatic_aberration': {'cyberpunk_neon': 0.9, 'rgb_glow': 0.8, 'soft_glow': 0.1},
    'vignette': {'film_grain': 0.9, 'cinematic': 0.9, 'dark_moody': 0.8},
    'soft_glow': {'dreamy_ethereal': 0.9, 'subtle_blur': 0.8, 'chromatic_aberration': 0.1},
    'rgb_glow': {'cyberpunk_neon': 0.9, 'chromatic_aberration': 0.8, 'electronic': 0.9}
}

# ========================================
# STYLE TEMPLATES (Complete Aesthetic Presets)
# ========================================
STYLE_TEMPLATES = {
    'auto': {
        'description': 'AI decides based on music analysis',
        'uses_music_analysis': True
    },
    'cinematic': {
        'description': 'Hollywood film aesthetic',
        'color_grade': 'cinematic_teal_orange',
        'effects': ['film_grain', 'vignette'],
        'transitions': ['fade', 'dissolve'],
        'max_concurrent_effects': 3,
        'intensity_range': (0.5, 0.8),
        'cut_frequency': 'medium'
    },
    'cyberpunk': {
        'description': 'Neon high-tech aesthetic',
        'color_grade': 'cyberpunk_neon',
        'effects': ['chromatic_aberration', 'rgb_glow'],
        'transitions': ['pixelize', 'circleopen'],
        'max_concurrent_effects': 3,
        'intensity_range': (0.6, 0.9),
        'cut_frequency': 'fast',
        'beat_effects': ['flash', 'pulse_scale']
    },
    'vintage': {
        'description': 'Nostalgic film look',
        'color_grade': 'vintage_film',
        'effects': ['film_grain', 'vignette'],
        'transitions': ['dissolve', 'fade'],
        'max_concurrent_effects': 2,
        'intensity_range': (0.4, 0.7),
        'cut_frequency': 'slow'
    },
    'dreamy': {
        'description': 'Ethereal soft aesthetic',
        'color_grade': 'dreamy_ethereal',
        'effects': ['soft_glow', 'subtle_blur'],
        'transitions': ['dissolve', 'fade'],
        'max_concurrent_effects': 2,
        'intensity_range': (0.3, 0.6),
        'cut_frequency': 'slow'
    },
    'energetic': {
        'description': 'High-energy dynamic',
        'color_grade': 'vibrant_pop',
        'effects': ['sharp_details'],
        'transitions': ['wipeleft', 'cut'],
        'max_concurrent_effects': 2,
        'intensity_range': (0.6, 0.9),
        'cut_frequency': 'very_fast',
        'beat_effects': ['flash']
    }
}

# ========================================
# COMPLETE EFFECTS LIBRARY
# ========================================
EFFECTS_LIBRARY = {
    'color_grades': COLOR_GRADES,
    'visual_fx': VISUAL_FX,
    'transitions': TRANSITIONS,
    'motion_fx': MOTION_FX,
    'beat_fx': BEAT_FX
}

# Helper function to get compatible effects
def get_compatible_effects(current_effects, category='visual_fx'):
    """
    Returns list of effects compatible with currently active effects
    
    Args:
        current_effects: List of currently active effect names
        category: Effect category to search in
        
    Returns:
        List of (effect_name, compatibility_score) tuples
    """
    if not current_effects:
        return list(EFFECTS_LIBRARY[category].keys())
    
    compatible = []
    for effect_name, effect_data in EFFECTS_LIBRARY[category].items():
        if effect_name in current_effects:
            continue
            
        avg_compatibility = 0.5  # Default neutral compatibility
        compatibilities = []
        
        for current_effect in current_effects:
            if current_effect in COMPATIBILITY_MATRIX.get(effect_name, {}):
                compatibilities.append(COMPATIBILITY_MATRIX[effect_name][current_effect])
        
        if compatibilities:
            avg_compatibility = sum(compatibilities) / len(compatibilities)
        
        # Check incompatible list
        if 'incompatible' in effect_data:
            if any(curr in effect_data['incompatible'] for curr in current_effects):
                continue
        
        if avg_compatibility > 0.5:
            compatible.append((effect_name, avg_compatibility))
    
    return sorted(compatible, key=lambda x: x[1], reverse=True)
