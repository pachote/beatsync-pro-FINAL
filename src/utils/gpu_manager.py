"""
?? Universal GPU Manager for BeatSync PRO
Detects any NVIDIA GPU (GTX 600+ to RTX 5090) or falls back to CPU
Automatically configures FFmpeg settings for optimal performance
"""

import subprocess
import platform
import re
from typing import Dict, Optional


class GPUManager:
    """Universal GPU detection and configuration"""
    
    # GPUs WITHOUT NVENC support
    NO_NVENC_GPUS = [
        'GT 610', 'GT 620', 'GT 630', 'GT 1030',
        'GTX 1650',  # Original (not SUPER/Ti)
        'MX150', 'MX250', 'MX350', 'MX450'
    ]
    
    def __init__(self):
        self.gpu_name = None
        self.has_nvenc = False
        self.use_cpu = False
        self.detect_gpu()
    
    def detect_gpu(self) -> Dict:
        """Detect GPU and determine capabilities"""
        
        # Try nvidia-smi first (most reliable)
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                capture_output=True, text=True, timeout=3
            )
            if result.returncode == 0 and result.stdout.strip():
                self.gpu_name = result.stdout.strip()
        except:
            pass
        
        # Fallback: Try WMIC (Windows)
        if not self.gpu_name and platform.system() == 'Windows':
            try:
                result = subprocess.run(
                    ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                    capture_output=True, text=True, timeout=3
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'NVIDIA' in line or 'GTX' in line or 'RTX' in line:
                            self.gpu_name = line.strip()
                            break
            except:
                pass
        
        if not self.gpu_name:
            print("??  No NVIDIA GPU detected, using CPU encoding")
            self.use_cpu = True
            return {'name': 'CPU', 'has_nvenc': False}
        
        # Check if GPU has NVENC
        self.has_nvenc = self._check_nvenc(self.gpu_name)
        
        if not self.has_nvenc:
            print(f"??  GPU '{self.gpu_name}' has no NVENC, using CPU encoding")
            self.use_cpu = True
        else:
            print(f"? GPU Detected: {self.gpu_name} (NVENC Enabled)")
        
        return {
            'name': self.gpu_name,
            'has_nvenc': self.has_nvenc
        }
    
    def _check_nvenc(self, gpu_name: str) -> bool:
        """Check if GPU has NVENC support"""
        
        # Check exclusion list
        for excluded in self.NO_NVENC_GPUS:
            if excluded in gpu_name:
                return False
        
        # GTX 600+ and RTX have NVENC
        if any(x in gpu_name for x in ['GTX', 'RTX', 'Quadro', 'Tesla']):
            match = re.search(r'(\d{3,4})', gpu_name)
            if match:
                model_num = int(match.group(1))
                if model_num >= 600:  # GTX 600 series (2012) and later
                    return True
        
        # Check via ffmpeg
        try:
            result = subprocess.run(
                ['ffmpeg', '-hide_banner', '-encoders'],
                capture_output=True, text=True, timeout=3
            )
            return 'h264_nvenc' in result.stdout
        except:
            pass
        
        return False
    
    def get_encoder_args(self) -> list:
        """Get FFmpeg encoder arguments for this system"""
        
        if self.use_cpu:
            # CPU encoding (x264 - works on ANY computer)
            return [
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-pix_fmt', 'yuv420p'
            ]
        else:
            # GPU encoding (NVENC - fast!)
            return [
                '-c:v', 'h264_nvenc',
                '-preset', 'p4',  # Balanced quality/speed
                '-rc', 'vbr',
                '-cq', '23',
                '-pix_fmt', 'yuv420p'
            ]


# Global instance
_gpu_manager = None

def get_gpu_manager() -> GPUManager:
    """Get or create GPU manager singleton"""
    global _gpu_manager
    if _gpu_manager is None:
        _gpu_manager = GPUManager()
    return _gpu_manager
