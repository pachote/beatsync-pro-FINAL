"""
BEATSYNC PRO - VIDEO THUMBNAIL EXTRACTOR
Extracts real video frames using FFmpeg for professional thumbnails
"""

import subprocess
import os
from pathlib import Path
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


class VideoThumbnailExtractor:
    """
    Professional video thumbnail extractor using FFmpeg
    Extracts high-quality frames for UI display
    """
    
    def __init__(self, cache_dir=None):
        """
        Initialize thumbnail extractor
        
        Args:
            cache_dir: Directory to cache thumbnails (optional)
        """
        self.cache_dir = cache_dir or Path("cache/thumbnails")
        self.cache_dir = Path(self.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # FFmpeg path (assuming it's in system PATH or local directory)
        self.ffmpeg_path = "ffmpeg"
    
    def extract_thumbnail(
        self, 
        video_path, 
        timestamp=1.0, 
        width=266, 
        height=150,
        use_cache=True
    ):
        """
        Extract a single frame from video at specified timestamp
        
        Args:
            video_path: Path to video file
            timestamp: Time in seconds to extract frame (default: 1.0s)
            width: Thumbnail width in pixels (default: 266px for 16:9)
            height: Thumbnail height in pixels (default: 150px)
            use_cache: Whether to use cached thumbnails (default: True)
        
        Returns:
            QPixmap: Extracted frame as QPixmap, or None on error
        """
        try:
            video_path = Path(video_path)
            
            if not video_path.exists():
                print(f"❌ Video file not found: {video_path}")
                return None
            
            # Generate cache filename
            cache_filename = f"{video_path.stem}_{timestamp}s_{width}x{height}.jpg"
            cache_path = self.cache_dir / cache_filename
            
            # Check cache first
            if use_cache and cache_path.exists():
                print(f"✅ Loading cached thumbnail: {cache_filename}")
                return QPixmap(str(cache_path))
            
            # Extract frame using FFmpeg
            print(f"🎬 Extracting thumbnail from: {video_path.name} at {timestamp}s")
            
            cmd = [
                self.ffmpeg_path,
                '-ss', str(timestamp),          # Seek to timestamp
                '-i', str(video_path),          # Input video
                '-vframes', '1',                # Extract 1 frame
                '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2',
                '-q:v', '2',                    # High quality JPEG
                '-y',                           # Overwrite if exists
                str(cache_path)
            ]
            
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"❌ FFmpeg error: {result.stderr}")
                return None
            
            # Load extracted frame
            if cache_path.exists():
                print(f"✅ Thumbnail extracted: {cache_filename}")
                return QPixmap(str(cache_path))
            else:
                print(f"❌ Thumbnail file not created")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"❌ FFmpeg timeout extracting thumbnail")
            return None
        except Exception as e:
            print(f"❌ Error extracting thumbnail: {str(e)}")
            return None
    
    def extract_multiple_thumbnails(
        self, 
        video_path, 
        timestamps=[1.0, 3.0, 5.0],
        width=266,
        height=150
    ):
        """
        Extract multiple frames from video at different timestamps
        
        Args:
            video_path: Path to video file
            timestamps: List of timestamps in seconds
            width: Thumbnail width
            height: Thumbnail height
        
        Returns:
            list: List of QPixmaps (None for failed extractions)
        """
        thumbnails = []
        for timestamp in timestamps:
            pixmap = self.extract_thumbnail(
                video_path, 
                timestamp, 
                width, 
                height
            )
            thumbnails.append(pixmap)
        return thumbnails
    
    def clear_cache(self):
        """Clear all cached thumbnails"""
        try:
            for file in self.cache_dir.glob("*.jpg"):
                file.unlink()
            print(f"✅ Thumbnail cache cleared")
        except Exception as e:
            print(f"❌ Error clearing cache: {str(e)}")
    
    def get_cache_size(self):
        """Get total size of cached thumbnails in bytes"""
        total_size = sum(
            f.stat().st_size 
            for f in self.cache_dir.glob("*.jpg")
        )
        return total_size
    
    @staticmethod
    def create_gradient_placeholder(width=266, height=150):
        """
        Create a gradient placeholder for videos without thumbnails
        
        Args:
            width: Placeholder width
            height: Placeholder height
        
        Returns:
            QPixmap: Gradient placeholder
        """
        from PySide6.QtGui import QLinearGradient, QPainter, QColor
        
        pixmap = QPixmap(width, height)
        painter = QPainter(pixmap)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0.0, QColor("#667eea"))
        gradient.setColorAt(1.0, QColor("#764ba2"))
        
        painter.fillRect(0, 0, width, height, gradient)
        painter.end()
        
        return pixmap


class VideoMetadataExtractor:
    """
    Extract video metadata using FFprobe
    """
    
    def __init__(self):
        self.ffprobe_path = "ffprobe"
    
    def get_video_info(self, video_path):
        """
        Get video metadata (duration, resolution, codec, fps)
        
        Args:
            video_path: Path to video file
        
        Returns:
            dict: Video metadata or None on error
        """
        try:
            cmd = [
                self.ffprobe_path,
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,codec_name,r_frame_rate,duration',
                '-show_entries', 'format=duration',
                '-of', 'json',
                str(video_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                # Extract info
                info = {}
                if 'streams' in data and len(data['streams']) > 0:
                    stream = data['streams'][0]
                    info['width'] = stream.get('width', 0)
                    info['height'] = stream.get('height', 0)
                    info['codec'] = stream.get('codec_name', 'unknown')
                    
                    # Parse frame rate
                    fps_str = stream.get('r_frame_rate', '0/1')
                    if '/' in fps_str:
                        num, den = map(int, fps_str.split('/'))
                        info['fps'] = round(num / den, 2) if den > 0 else 0
                    else:
                        info['fps'] = 0
                    
                    # Duration
                    info['duration'] = float(stream.get('duration', 0))
                
                if 'format' in data and 'duration' in data['format']:
                    if 'duration' not in info or info['duration'] == 0:
                        info['duration'] = float(data['format']['duration'])
                
                return info
            else:
                print(f"❌ FFprobe error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting video info: {str(e)}")
            return None
    
    def get_video_duration(self, video_path):
        """
        Get video duration in seconds
        
        Args:
            video_path: Path to video file
        
        Returns:
            float: Duration in seconds, or 0 on error
        """
        info = self.get_video_info(video_path)
        return info.get('duration', 0) if info else 0
    
    def format_duration(self, seconds):
        """
        Format duration as MM:SS
        
        Args:
            seconds: Duration in seconds
        
        Returns:
            str: Formatted duration (e.g., "3:45")
        """
        if seconds <= 0:
            return "0:00"
        
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"


# Global instances for easy access
thumbnail_extractor = VideoThumbnailExtractor()
metadata_extractor = VideoMetadataExtractor()


# ═══════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════

def extract_video_thumbnail(video_path, timestamp=1.0, width=266, height=150):
    """
    Quick function to extract a video thumbnail
    
    Args:
        video_path: Path to video file
        timestamp: Time in seconds (default: 1.0s)
        width: Thumbnail width (default: 266px)
        height: Thumbnail height (default: 150px)
    
    Returns:
        QPixmap or None
    """
    return thumbnail_extractor.extract_thumbnail(
        video_path, 
        timestamp, 
        width, 
        height
    )


def get_video_duration(video_path):
    """
    Quick function to get video duration
    
    Args:
        video_path: Path to video file
    
    Returns:
        float: Duration in seconds
    """
    return metadata_extractor.get_video_duration(video_path)


def format_duration(seconds):
    """
    Quick function to format duration
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        str: Formatted duration (MM:SS)
    """
    return metadata_extractor.format_duration(seconds)
