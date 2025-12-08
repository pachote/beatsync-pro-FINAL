"""Centralized audio file management - fixes file tracking and sorting"""
import os
from pathlib import Path
from datetime import datetime
from PySide6.QtCore import QObject, Signal

class AudioManager(QObject):
    # Signals
    file_added = Signal(str)
    file_removed = Signal(str)
    current_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.audio_files = {}  # basename -> full_path
        self.current_file = None
        self.analyses = {}  # path -> analysis object
        
    def add_file(self, file_path):
        """Add audio file with proper tracking"""
        if not os.path.exists(file_path):
            print(f"[AudioManager] File does not exist: {file_path}")
            return False
        
        basename = os.path.basename(file_path)
        self.audio_files[basename] = file_path
        print(f"[AudioManager] Added file: {basename} -> {file_path}")
        self.file_added.emit(file_path)
        return True
    
    def get_sorted_files(self):
        """Get files sorted by newest first - FIXES SORTING ISSUE"""
        items = []
        for basename, path in self.audio_files.items():
            if os.path.exists(path):
                mod_time = os.path.getmtime(path)
                items.append((basename, path, mod_time))
            else:
                print(f"[AudioManager] Warning: File no longer exists: {path}")
        
        # Sort by modification time, newest first
        items.sort(key=lambda x: x[2], reverse=True)
        print(f"[AudioManager] Sorted {len(items)} files by date (newest first)")
        return items
    
    def get_file_path(self, basename):
        """Get full path from basename"""
        return self.audio_files.get(basename)
    
    def set_current(self, file_path):
        """Set current audio file"""
        if file_path in self.audio_files.values():
            self.current_file = file_path
            print(f"[AudioManager] Set current file: {os.path.basename(file_path)}")
            self.current_changed.emit(file_path)
            return True
        else:
            print(f"[AudioManager] File not in manager: {file_path}")
            return False
    
    def get_current(self):
        """Get current audio file path"""
        return self.current_file
    
    def store_analysis(self, file_path, analysis):
        """Store analysis for a file"""
        self.analyses[file_path] = analysis
        print(f"[AudioManager] Stored analysis for: {os.path.basename(file_path)}")
    
    def get_analysis(self, file_path):
        """Get stored analysis for a file"""
        return self.analyses.get(file_path)
    
    def clear(self):
        """Clear all files and analyses"""
        self.audio_files.clear()
        self.analyses.clear()
        self.current_file = None
        print("[AudioManager] Cleared all files and analyses")
