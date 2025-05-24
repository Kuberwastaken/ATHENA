"""
Wake Word Detection System for Project ATHENA

This module handles detection of wake words to activate the voice assistant.
It uses a lightweight model to continuously monitor the audio stream for
specified trigger phrases.
"""

import numpy as np
import threading
import time
import queue
import logging
from enum import Enum

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("wake_word")

class DetectionState(Enum):
    INACTIVE = 0
    LISTENING = 1
    DETECTED = 2

class WakeWordDetector:
    """
    Wake word detection system that continuously monitors audio input
    for specified trigger phrases.
    """
    
    def __init__(self, 
                 model_path="models/wake_word_model.pth", 
                 device="cpu",
                 trigger_threshold=0.8,
                 sample_rate=16000):
        """
        Initialize the wake word detector.
        
        Args:
            model_path: Path to the wake word model file
            device: Device to run the model on ("cpu" or "cuda")
            trigger_threshold: Confidence threshold for detection
            sample_rate: Audio sample rate
        """
        self.model_path = model_path
        self.device = device
        self.trigger_threshold = trigger_threshold
        self.sample_rate = sample_rate
        
        self.audio_queue = queue.Queue()
        self.detection_callback = None
        self.state = DetectionState.INACTIVE
        self.running = False
        self.detection_thread = None
        
        logger.info(f"Initializing wake word detector with model: {model_path}")
        self._load_model()
        
    def _load_model(self):
        """Load the wake word detection model."""
        try:
            # This is a placeholder for actual model loading code
            # In a real implementation, this would use PyTorch, TensorFlow, or another ML framework
            logger.info("Loading wake word model...")
            time.sleep(1)  # Simulate loading time
            logger.info("Model loaded successfully")
            self.model = None  # Placeholder for the actual model
            
        except Exception as e:
            logger.error(f"Failed to load wake word model: {e}")
            raise RuntimeError(f"Failed to load wake word model: {e}")
    
    def start(self, detection_callback=None):
        """
        Start the wake word detection process.
        
        Args:
            detection_callback: Function to call when wake word is detected
                               Function signature: callback(confidence_score)
        """
        if self.running:
            logger.warning("Wake word detector is already running")
            return
            
        self.running = True
        self.state = DetectionState.LISTENING
        self.detection_callback = detection_callback
        
        # Start the detection thread
        self.detection_thread = threading.Thread(target=self._detection_loop)
        self.detection_thread.daemon = True
        self.detection_thread.start()
        
        logger.info("Wake word detector started")
        
    def stop(self):
        """Stop the wake word detection process."""
        if not self.running:
            logger.warning("Wake word detector is not running")
            return
            
        self.running = False
        if self.detection_thread:
            self.detection_thread.join(timeout=2.0)
        self.state = DetectionState.INACTIVE
        
        logger.info("Wake word detector stopped")
        
    def process_audio(self, audio_frame):
        """
        Process an audio frame for wake word detection.
        
        Args:
            audio_frame: Audio data as numpy array
        """
        if self.running:
            self.audio_queue.put(audio_frame)
            
    def _detection_loop(self):
        """Main detection loop that runs in a separate thread."""
        logger.info("Detection loop started")
        
        buffer_size = int(self.sample_rate * 1.5)  # 1.5 seconds buffer
        audio_buffer = np.zeros(buffer_size, dtype=np.float32)
        
        while self.running:
            try:
                # Get audio frame from queue with timeout
                frame = self.audio_queue.get(timeout=0.1)
                
                # Update buffer (slide window)
                frame_size = len(frame)
                audio_buffer = np.roll(audio_buffer, -frame_size)
                audio_buffer[-frame_size:] = frame
                
                # Detect wake word
                confidence = self._detect_wake_word(audio_buffer)
                
                if confidence > self.trigger_threshold:
                    logger.info(f"Wake word detected with confidence: {confidence:.2f}")
                    self.state = DetectionState.DETECTED
                    
                    # Call detection callback if provided
                    if self.detection_callback:
                        self.detection_callback(confidence)
                        
                    # Small pause after detection to avoid multiple triggers
                    time.sleep(1.0)
                    self.state = DetectionState.LISTENING
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in detection loop: {e}")
                
        logger.info("Detection loop ended")
                
    def _detect_wake_word(self, audio_buffer):
        """
        Detect wake word in the audio buffer.
        
        Args:
            audio_buffer: Audio data as numpy array
            
        Returns:
            float: Confidence score (0.0 to 1.0)
        """
        # This is a placeholder for actual detection code
        # In a real implementation, this would process the audio with the loaded model
        
        # Simulate detection with random confidence (for demonstration)
        # Replace with actual model inference
        confidence = np.random.random() * 0.3  # Mostly low values to avoid false triggers
        
        # Every ~100 calls, simulate a detection for testing
        if np.random.random() < 0.01:
            confidence = np.random.uniform(0.85, 0.95)
            
        return confidence
        
    def get_state(self):
        """Get the current state of the detector."""
        return self.state
        
    def set_sensitivity(self, threshold):
        """
        Set the detection sensitivity.
        
        Args:
            threshold: New confidence threshold (0.0 to 1.0)
        """
        if 0.0 <= threshold <= 1.0:
            self.trigger_threshold = threshold
            logger.info(f"Detection threshold set to {threshold:.2f}")
        else:
            logger.error(f"Invalid threshold value: {threshold}")
            

# Example usage
if __name__ == "__main__":
    def on_wake_word(confidence):
        print(f"Wake word detected! Confidence: {confidence:.2f}")
        
    # Create and start the detector
    detector = WakeWordDetector()
    detector.start(detection_callback=on_wake_word)
    
    try:
        # Simulate sending audio frames
        print("Simulating audio input (press Ctrl+C to stop)...")
        while True:
            # In a real application, this would be actual microphone data
            fake_audio = np.random.random(1600).astype(np.float32) * 0.1
            detector.process_audio(fake_audio)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nStopping...")
        
    finally:
        detector.stop()
        print("Wake word detector stopped.")
