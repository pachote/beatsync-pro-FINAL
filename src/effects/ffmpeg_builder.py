"""
FFmpeg Complex Filter Chain Builder
Translates high-level effect decisions into executable FFmpeg filter chains
"""

import os
from typing import List, Dict, Tuple
from .effects_library import EFFECTS_LIBRARY, STYLE_TEMPLATES

class FFmpegFilterBuilder:
    """
    Builds complex FFmpeg filter chains from effect decisions
    Handles layering, timing, transitions, and beat synchronization
    """
    
    def __init__(self):
        self.video_filters = []
        self.audio_filters = []
        self.labels = {}
        self.input_count = 0
        
    def reset(self):
        """Clear all filters for new build"""
        self.video_filters = []
        self.audio_filters = []
        self.labels = {}
        self.input_count = 0
    
    def add_scale(self, width=1920, height=1080, label_out='scaled'):
        """Normalize video resolution"""
        filter_str = f"scale={width}:{height}"
        self.video_filters.append(f"[{self.input_count}:v]{filter_str}[{label_out}]")
        self.labels['last_video'] = label_out
        return label_out
    
    def add_color_grade(self, grade_name, intensity=1.0, label_in=None, label_out='graded'):
        """
        Apply color grading from library
        
        Args:
            grade_name: Name from COLOR_GRADES
            intensity: 0.0-1.0 multiplier for effect strength
            label_in: Input stream label (uses last if None)
            label_out: Output stream label
        """
        if grade_name not in EFFECTS_LIBRARY['color_grades']:
            print(f"Warning: Color grade '{grade_name}' not found")
            return label_in
        
        grade = EFFECTS_LIBRARY['color_grades'][grade_name]
        filter_str = grade['ffmpeg_filter']
        
        # Adjust intensity if needed (simplified - real implementation would parse and adjust)
        if intensity < 1.0:
            # For now, just apply as-is (proper intensity scaling would parse the filter)
            pass
        
        if label_in is None:
            label_in = self.labels.get('last_video', '0:v')
        
        self.video_filters.append(f"[{label_in}]{filter_str}[{label_out}]")
        self.labels['last_video'] = label_out
        return label_out
    
    def add_visual_effect(self, fx_name, params=None, label_in=None, label_out=None):
        """
        Apply visual effect from library
        
        Args:
            fx_name: Name from VISUAL_FX
            params: Dict of parameters to override defaults
            label_in: Input stream label
            label_out: Output stream label
        """
        if fx_name not in EFFECTS_LIBRARY['visual_fx']:
            print(f"Warning: Visual effect '{fx_name}' not found")
            return label_in
        
        fx = EFFECTS_LIBRARY['visual_fx'][fx_name]
        filter_template = fx['ffmpeg_filter']
        
        # Merge default params with provided params
        effect_params = fx.get('default_params', {}).copy()
        if params:
            effect_params.update(params)
        
        # Format filter string with parameters
        filter_str = filter_template.format(**effect_params)
        
        if label_in is None:
            label_in = self.labels.get('last_video', '0:v')
        if label_out is None:
            label_out = f"{fx_name}_out"
        
        # Handle complex filters (like glow with split/blend)
        if 'split' in filter_str:
            # This is a complex multi-stage filter, add as-is
            self.video_filters.append(f"[{label_in}]{filter_str}[{label_out}]")
        else:
            # Simple single filter
            self.video_filters.append(f"[{label_in}]{filter_str}[{label_out}]")
        
        self.labels['last_video'] = label_out
        return label_out
    
    def add_beat_flash(self, beat_time, duration=0.05, intensity=2.0):
        """
        Add flash effect at specific beat time
        
        Args:
            beat_time: Time in seconds where beat occurs
            duration: Flash duration in seconds
            intensity: Contrast multiplier
        """
        end_time = beat_time + duration
        filter_str = f"eq=contrast={intensity}:enable='between(t,{beat_time:.3f},{end_time:.3f})'"
        
        # Beat effects are chained onto existing filters with commas
        if self.video_filters:
            # Append to last filter with comma
            self.video_filters[-1] = self.video_filters[-1].replace(']', f',{filter_str}]')
        else:
            # First filter
            label_in = self.labels.get('last_video', '0:v')
            self.video_filters.append(f"[{label_in}]{filter_str}[beat_out]")
            self.labels['last_video'] = 'beat_out'
    
    def add_transition(self, transition_type, duration, offset, input_label_a, input_label_b, output_label):
        """
        Add transition between two clips
        
        Args:
            transition_type: Type from TRANSITIONS
            duration: Transition duration in seconds
            offset: Time offset where transition starts
            input_label_a: First clip label
            input_label_b: Second clip label
            output_label: Output label after transition
        """
        if transition_type == 'cut':
            # No transition, just concatenation
            return
        
        if transition_type not in EFFECTS_LIBRARY['transitions']:
            print(f"Warning: Transition '{transition_type}' not found, using fade")
            transition_type = 'fade'
        
        trans = EFFECTS_LIBRARY['transitions'][transition_type]
        filter_str = trans['ffmpeg_filter'].format(
            duration=duration,
            offset=offset
        )
        
        self.video_filters.append(f"[{input_label_a}][{input_label_b}]{filter_str}[{output_label}]")
        self.labels['last_video'] = output_label
        return output_label
    
    def build_filter_complex(self):
        """
        Build complete filter_complex string from all added filters
        
        Returns:
            Complete filter_complex string ready for FFmpeg
        """
        if not self.video_filters:
            return None
        
        return ';'.join(self.video_filters)
    
    def build_clip_processing_command(self, input_file, output_file, trim_start=0, trim_duration=None):
        """
        Build complete FFmpeg command for processing a single clip
        
        Args:
            input_file: Input video path
            output_file: Output video path
            trim_start: Start time for trimming
            trim_duration: Duration to extract (None = full video)
            
        Returns:
            List of command arguments for subprocess
        """
        cmd = ['ffmpeg', '-i', input_file]
        
        # Add trim parameters
        if trim_start > 0:
            cmd.extend(['-ss', str(trim_start)])
        if trim_duration:
            cmd.extend(['-t', str(trim_duration)])
        
        # Add filter complex if we have filters
        filter_str = self.build_filter_complex()
        if filter_str:
            cmd.extend(['-filter_complex', filter_str])
            # Map the final output
            final_label = self.labels.get('last_video', 'v')
            cmd.extend(['-map', f'[{final_label}]'])
        
        # Output settings
        cmd.extend([
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-y',  # Overwrite output
            output_file
        ])
        
        return cmd
    
    def build_concatenation_command(self, input_files, output_file, with_transitions=True):
        """
        Build command to concatenate multiple processed clips
        
        Args:
            input_files: List of processed clip paths
            output_file: Final output path
            with_transitions: Whether to add transitions between clips
            
        Returns:
            FFmpeg command arguments
        """
        if len(input_files) == 1:
            # Single file, just copy
            return ['ffmpeg', '-i', input_files[0], '-c', 'copy', '-y', output_file]
        
        # Create concat file
        concat_list_path = os.path.join(os.path.dirname(output_file), 'concat_list.txt')
        with open(concat_list_path, 'w') as f:
            for input_file in input_files:
                f.write(f"file '{input_file}'\n")
        
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_list_path,
            '-c', 'copy',
            '-y',
            output_file
        ]
        
        return cmd
    
    def build_audio_overlay_command(self, video_file, audio_file, output_file):
        """
        Overlay audio track on video
        
        Args:
            video_file: Video file path
            audio_file: Audio file path
            output_file: Output file path
            
        Returns:
            FFmpeg command arguments
        """
        cmd = [
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',  # End when shortest stream ends
            '-y',
            output_file
        ]
        
        return cmd

# ========================================
# HELPER FUNCTIONS
# ========================================

def create_clip_plan_from_template(style_name, clip_duration, beat_times=None):
    """
    Create effect plan for a clip based on style template
    
    Args:
        style_name: Name from STYLE_TEMPLATES
        clip_duration: Duration of clip in seconds
        beat_times: List of beat times within clip (optional)
        
    Returns:
        Dict of effect parameters
    """
    if style_name not in STYLE_TEMPLATES:
        style_name = 'cinematic'  # Default fallback
    
    template = STYLE_TEMPLATES[style_name]
    
    plan = {
        'color_grade': template.get('color_grade'),
        'effects': template.get('effects', []),
        'intensity_range': template.get('intensity_range', (0.5, 0.8)),
        'beat_effects': []
    }
    
    # Add beat effects if available and beats provided
    if beat_times and 'beat_effects' in template:
        for beat_time in beat_times:
            if beat_time < clip_duration:
                plan['beat_effects'].append({
                    'type': template['beat_effects'][0],  # Use first beat effect type
                    'time': beat_time
                })
    
    return plan
