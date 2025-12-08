"""
BeatSync PRO - License Manager
Handles local storage and validation of license keys
"""
import json
import base64
from pathlib import Path
from typing import Optional, Dict, Any
import os

class LicenseManager:
    """Manages license key storage and validation state"""
    
    def __init__(self):
        # Store in user's AppData for persistence
        self.config_dir = Path(os.environ.get('APPDATA', Path.home())) / 'BeatSyncPRO'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.license_file = self.config_dir / '.license'
        self.cached_key: Optional[str] = None
        self.cached_email: Optional[str] = None
        self.cached_tier: Optional[str] = None
        
    def _encode(self, data: str) -> str:
        """Simple obfuscation (not true encryption)"""
        return base64.b64encode(data.encode()).decode()
    
    def _decode(self, data: str) -> str:
        """Decode obfuscated data"""
        try:
            return base64.b64decode(data.encode()).decode()
        except:
            return ""
    
    def save_license(self, license_key: str, email: str = "", tier: str = "") -> bool:
        """Save license key locally"""
        try:
            data = {
                "key": self._encode(license_key),
                "email": self._encode(email),
                "tier": self._encode(tier)
            }
            with open(self.license_file, 'w') as f:
                json.dump(data, f)
            self.cached_key = license_key
            self.cached_email = email
            self.cached_tier = tier
            return True
        except Exception as e:
            print(f"Failed to save license: {e}")
            return False
    
    def load_license(self) -> Optional[str]:
        """Load saved license key"""
        if self.cached_key:
            return self.cached_key
        try:
            if self.license_file.exists():
                with open(self.license_file, 'r') as f:
                    data = json.load(f)
                self.cached_key = self._decode(data.get("key", ""))
                self.cached_email = self._decode(data.get("email", ""))
                self.cached_tier = self._decode(data.get("tier", ""))
                return self.cached_key if self.cached_key else None
        except Exception as e:
            print(f"Failed to load license: {e}")
        return None
    
    def get_cached_email(self) -> str:
        """Get cached email"""
        if not self.cached_email:
            self.load_license()
        return self.cached_email or ""
    
    def get_cached_tier(self) -> str:
        """Get cached tier"""
        if not self.cached_tier:
            self.load_license()
        return self.cached_tier or ""
    
    def clear_license(self) -> bool:
        """Remove saved license"""
        try:
            if self.license_file.exists():
                self.license_file.unlink()
            self.cached_key = None
            self.cached_email = None
            self.cached_tier = None
            return True
        except:
            return False
    
    def has_saved_license(self) -> bool:
        """Check if a license is saved locally"""
        return self.load_license() is not None
