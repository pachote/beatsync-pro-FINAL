"""
BeatSync Pro Backend Connector
Memory-safe communication layer using weak references
Prevents circular references and memory leaks
"""

import weakref
import logging
from typing import Optional, Any, Dict, Callable, List
from dataclasses import dataclass
from enum import Enum
from PySide6.QtCore import QObject, Signal, Slot, QThread

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """Types of messages between frontend and backend"""
    VIDEO_LOAD = "video_load"
    VIDEO_PROCESS = "video_process"
    AUDIO_ANALYZE = "audio_analyze"
    BEAT_DETECT = "beat_detect"
    EXPORT_START = "export_start"
    EXPORT_PROGRESS = "export_progress"
    EXPORT_COMPLETE = "export_complete"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"

@dataclass
class Message:
    """Message structure for communication"""
    type: MessageType
    data: Any
    callback: Optional[Callable] = None
    error_callback: Optional[Callable] = None

class BackendWorker(QThread):
    """Worker thread for backend operations"""
    
    # Signals
    progress = Signal(int)
    finished = Signal(dict)
    error = Signal(str)
    message = Signal(Message)
    
    def __init__(self, task_type: str, task_data: Any):
        super().__init__()
        self.task_type = task_type
        self.task_data = task_data
        self._is_running = True
    
    def run(self):
        """Execute backend task"""
        try:
            # Simulate different task types
            if self.task_type == "beat_detection":
                self.detect_beats()
            elif self.task_type == "video_export":
                self.export_video()
            elif self.task_type == "effect_render":
                self.render_effects()
            else:
                logger.warning(f"Unknown task type: {self.task_type}")
                
        except Exception as e:
            logger.error(f"Worker error: {e}")
            self.error.emit(str(e))
    
    def detect_beats(self):
        """Simulate beat detection"""
        for i in range(101):
            if not self._is_running:
                break
            self.progress.emit(i)
            QThread.msleep(10)  # Simulate processing
        
        self.finished.emit({
            'beats': [0.5, 1.0, 1.5, 2.0],  # Sample beat times
            'bpm': 120,
            'confidence': 0.963
        })
    
    def export_video(self):
        """Simulate video export"""
        for i in range(101):
            if not self._is_running:
                break
            self.progress.emit(i)
            QThread.msleep(20)  # Simulate export
        
        self.finished.emit({'output_file': 'output.mp4'})
    
    def render_effects(self):
        """Simulate effect rendering"""
        for i in range(101):
            if not self._is_running:
                break
            self.progress.emit(i)
            QThread.msleep(5)  # Simulate rendering
        
        self.finished.emit({'rendered_frames': 1000})
    
    def stop(self):
        """Stop the worker thread"""
        self._is_running = False

class BackendConnector(QObject):
    """
    Memory-safe backend connector using weak references
    Manages communication between UI and processing backend
    """
    
    # Signals for UI updates
    processing_started = Signal(str)
    processing_progress = Signal(str, int)
    processing_complete = Signal(str, dict)
    processing_error = Signal(str, str)
    
    # Status signals
    backend_ready = Signal()
    backend_busy = Signal(bool)
    memory_warning = Signal(float)
    
    def __init__(self, main_window_ref=None):
        """
        Initialize with weak reference to main window
        
        Args:
            main_window_ref: Weak reference to main window or None
        """
        super().__init__()
        
        # CRITICAL: Store as weak reference to prevent circular references
        self._main_window_ref = main_window_ref
        
        # Active workers (store strong references while running)
        self.active_workers: Dict[str, BackendWorker] = {}
        
        # Message queue
        self.message_queue: List[Message] = []
        
        # Callbacks storage (weak references)
        self._callbacks: Dict[str, List[weakref.ref]] = {}
        
        # Backend state
        self.is_initialized = False
        self.is_busy = False
        
        # Initialize backend
        self.initialize_backend()
        
        logger.info("BackendConnector initialized with weak references")
    
    @property
    def main_window(self):
        """Get main window from weak reference"""
        if self._main_window_ref:
            window = self._main_window_ref()
            if window is None:
                logger.warning("Main window reference is dead")
            return window
        return None
    
    def initialize_backend(self):
        """Initialize backend systems"""
        try:
            # Initialize video pipeline
            self._init_video_pipeline()
            
            # Initialize audio pipeline
            self._init_audio_pipeline()
            
            # Initialize AI models (lazy loading)
            self._init_ai_models()
            
            self.is_initialized = True
            self.backend_ready.emit()
            
            logger.info("Backend systems initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize backend: {e}")
            self.processing_error.emit("initialization", str(e))
    
    def _init_video_pipeline(self):
        """Initialize video processing pipeline"""
        # Placeholder for video pipeline initialization
        logger.info("Video pipeline ready")
    
    def _init_audio_pipeline(self):
        """Initialize audio processing pipeline"""
        # Placeholder for audio pipeline initialization
        logger.info("Audio pipeline ready")
    
    def _init_ai_models(self):
        """Initialize AI models (lazy loading)"""
        # Models will be loaded on-demand to save memory
        logger.info("AI models ready for lazy loading")
    
    def register_callback(self, event: str, callback: Callable):
        """
        Register callback with weak reference
        
        Args:
            event: Event name
            callback: Callback function
        """
        if event not in self._callbacks:
            self._callbacks[event] = []
        
        # Store as weak reference
        weak_callback = weakref.ref(callback)
        self._callbacks[event].append(weak_callback)
        
        logger.debug(f"Registered callback for event: {event}")
    
    def unregister_callback(self, event: str, callback: Callable):
        """Unregister callback"""
        if event in self._callbacks:
            # Remove dead references and the specified callback
            self._callbacks[event] = [
                ref for ref in self._callbacks[event]
                if ref() is not None and ref() != callback
            ]
    
    def emit_event(self, event: str, data: Any = None):
        """
        Emit event to registered callbacks
        
        Args:
            event: Event name
            data: Event data
        """
        if event in self._callbacks:
            # Clean up dead references
            alive_callbacks = []
            
            for callback_ref in self._callbacks[event]:
                callback = callback_ref()
                if callback is not None:
                    alive_callbacks.append(callback_ref)
                    try:
                        callback(data)
                    except Exception as e:
                        logger.error(f"Callback error for {event}: {e}")
            
            # Update with only alive callbacks
            self._callbacks[event] = alive_callbacks
    
    @Slot(str, dict)
    def process_request(self, request_type: str, parameters: Dict[str, Any]):
        """
        Process request from UI
        
        Args:
            request_type: Type of request
            parameters: Request parameters
        """
        logger.info(f"Processing request: {request_type}")
        
        # Check if already busy
        if self.is_busy and request_type not in ['cancel', 'status']:
            logger.warning("Backend is busy, queueing request")
            self.message_queue.append(Message(
                type=MessageType.INFO,
                data={'request': request_type, 'parameters': parameters}
            ))
            return
        
        # Create worker for the task
        worker = BackendWorker(request_type, parameters)
        
        # Connect signals
        worker.progress.connect(
            lambda p: self.processing_progress.emit(request_type, p)
        )
        worker.finished.connect(
            lambda d: self._on_worker_finished(request_type, d)
        )
        worker.error.connect(
            lambda e: self.processing_error.emit(request_type, e)
        )
        
        # Store worker reference
        self.active_workers[request_type] = worker
        
        # Update state
        self.is_busy = True
        self.backend_busy.emit(True)
        self.processing_started.emit(request_type)
        
        # Start processing
        worker.start()
    
    def _on_worker_finished(self, task_type: str, result: dict):
        """Handle worker completion"""
        logger.info(f"Worker finished: {task_type}")
        
        # Remove from active workers
        if task_type in self.active_workers:
            worker = self.active_workers.pop(task_type)
            worker.deleteLater()
        
        # Update state
        if not self.active_workers:
            self.is_busy = False
            self.backend_busy.emit(False)
        
        # Emit completion
        self.processing_complete.emit(task_type, result)
        
        # Process queued messages
        if self.message_queue and not self.is_busy:
            message = self.message_queue.pop(0)
            if message.type == MessageType.INFO:
                data = message.data
                self.process_request(data['request'], data['parameters'])
    
    @Slot(str)
    def cancel_processing(self, task_type: str = None):
        """
        Cancel processing task
        
        Args:
            task_type: Specific task to cancel or None for all
        """
        if task_type and task_type in self.active_workers:
            worker = self.active_workers[task_type]
            worker.stop()
            worker.wait()
            self.active_workers.pop(task_type)
            logger.info(f"Cancelled task: {task_type}")
            
        elif task_type is None:
            # Cancel all tasks
            for task, worker in list(self.active_workers.items()):
                worker.stop()
                worker.wait()
                logger.info(f"Cancelled task: {task}")
            
            self.active_workers.clear()
        
        # Update state
        if not self.active_workers:
            self.is_busy = False
            self.backend_busy.emit(False)
    
    def check_memory(self) -> float:
        """
        Check memory usage and emit warning if needed
        
        Returns:
            Current memory usage in MB
        """
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            # Check threshold
            total_memory = psutil.virtual_memory().total / 1024 / 1024
            usage_percent = (memory_mb / total_memory) * 100
            
            if usage_percent > 65:
                self.memory_warning.emit(memory_mb)
                logger.warning(f"High memory usage: {memory_mb:.1f} MB ({usage_percent:.1f}%)")
            
            return memory_mb
            
        except Exception as e:
            logger.error(f"Error checking memory: {e}")
            return 0.0
    
    def cleanup(self):
        """Clean up resources and references"""
        logger.info("Cleaning up BackendConnector")
        
        # Cancel all active tasks
        self.cancel_processing()
        
        # Clear callbacks
        self._callbacks.clear()
        
        # Clear message queue
        self.message_queue.clear()
        
        # Clear main window reference
        self._main_window_ref = None
        
        logger.info("BackendConnector cleanup complete")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        try:
            self.cleanup()
        except Exception as e:
            logger.error(f"Error in BackendConnector destructor: {e}")