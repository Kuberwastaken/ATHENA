"""
Microphone Array Interface for Project ATHENA

This module handles interfacing with the ReSpeaker 6-mic array,
managing audio streams, and preprocessing audio data.
"""

import numpy as np
import threading
import time
import queue
import logging
import sounddevice as sd

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("microphone")

class MicrophoneArray:
    """
    Interface for the ReSpeaker 6-mic circular array or similar microphone arrays.
    Handles audio capture, channel mixing, and basic preprocessing.
    """
    
    def __init__(self, 
                 device_name=None,
                 sample_rate=16000, 
                 channels=6,
                 chunk_size=1024):
        """
        Initialize the microphone array interface.
        
        Args:
            device_name: Name or part of name of the audio input device
            sample_rate: Audio sample rate to use
            channels: Number of microphone channels
            chunk_size: Audio chunk size in samples
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.device_name = device_name
        self.device_id = None
        
        self.audio_queue = queue.Queue(maxsize=100)
        self.callbacks = []
        self.running = False
        self.capture_thread = None
        
        # Find the audio device
        self._find_audio_device()
        
    def _find_audio_device(self):
        """Find the audio input device by name."""
        try:
            devices = sd.query_devices()
            logger.info(f"Available audio devices:")
            
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:  # Input devices only
                    logger.info(f"  {i}: {device['name']} (Inputs: {device['max_input_channels']})")
                    
                    # If device name is specified, try to match it
                    if self.device_name and self.device_name.lower() in device['name'].lower():
                        self.device_id = i
                        logger.info(f"Selected device {i}: {device['name']}")
                        break
            
            # If no device found but name was specified, warn user
            if self.device_name and self.device_id is None:
                logger.warning(f"No device found matching '{self.device_name}'. Will use default.")
                
            # If no device was specified or found, use default
            if self.device_id is None:
                self.device_id = sd.default.device[0]
                device_info = sd.query_devices(self.device_id)
                logger.info(f"Using default input device {self.device_id}: {device_info['name']}")
                
        except Exception as e:
            logger.error(f"Error finding audio device: {e}")
            raise RuntimeError(f"Failed to find audio device: {e}")
    
    def start_capture(self):
        """Start audio capture from the microphone array."""
        if self.running:
            logger.warning("Audio capture is already running")
            return
            
        self.running = True
        
        # Start the capture thread
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
        logger.info("Audio capture started")
        
    def stop_capture(self):
        """Stop audio capture."""
        if not self.running:
            logger.warning("Audio capture is not running")
            return
            
        self.running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2.0)
            
        logger.info("Audio capture stopped")
    
    def add_audio_callback(self, callback):
        """
        Add a callback function to receive audio data.
        
        Args:
            callback: Function that accepts a numpy array of audio data
                     Function signature: callback(audio_data, channel_data)
                     where audio_data is the mixed mono audio and channel_data
                     is the multi-channel raw data
        """
        if callback not in self.callbacks:
            self.callbacks.append(callback)
    
    def remove_audio_callback(self, callback):
        """Remove a previously added callback function."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback function for the sounddevice input stream."""
        if status:
            logger.warning(f"Audio callback status: {status}")
            
        # Put the audio data in the queue
        try:
            self.audio_queue.put_nowait(indata.copy())
        except queue.Full:
            logger.warning("Audio queue is full, dropping audio frame")
    
    def _capture_loop(self):
        """Main audio capture loop that runs in a separate thread."""
        logger.info("Audio capture loop started")
        
        try:
            with sd.InputStream(device=self.device_id,
                               channels=self.channels,
                               samplerate=self.sample_rate,
                               blocksize=self.chunk_size,
                               callback=self._audio_callback):
                
                logger.info(f"Audio stream opened with {self.channels} channels at {self.sample_rate}Hz")
                
                # Keep the thread alive
                while self.running:
                    # Process the queue
                    try:
                        # Get audio data from queue with timeout
                        audio_data = self.audio_queue.get(timeout=0.1)
                        
                        # Process the audio data
                        mono_audio = self._process_audio(audio_data)
                        
                        # Call all registered callbacks
                        for callback in self.callbacks:
                            callback(mono_audio, audio_data)
                            
                    except queue.Empty:
                        continue
                    except Exception as e:
                        logger.error(f"Error in audio processing: {e}")
                        
        except Exception as e:
            logger.error(f"Error in audio capture: {e}")
            self.running = False
            
        logger.info("Audio capture loop ended")
    
    def _process_audio(self, audio_data):
        """
        Process multi-channel audio data into a single channel.
        
        Args:
            audio_data: Multi-channel audio data as numpy array
            
        Returns:
            numpy.ndarray: Processed single-channel audio data
        """
        # Basic processing: average all channels to create mono audio
        # In a more sophisticated implementation, we'd do beamforming here
        mono_audio = np.mean(audio_data, axis=1).astype(np.float32)
        
        # Normalize
        if np.abs(mono_audio).max() > 0:
            mono_audio = mono_audio / np.abs(mono_audio).max()
            
        return mono_audio

    def get_sample_rate(self):
        """Get the current sample rate."""
        return self.sample_rate
        
    def get_channels(self):
        """Get the number of channels."""
        return self.channels
        

# Example usage
if __name__ == "__main__":
    def audio_handler(mono_audio, channel_data):
        # Simple level meter
        level = np.abs(mono_audio).mean() * 100
        bars = int(level * 50)
        print(f"\rLevel: {'█' * bars}{' ' * (50 - bars)} {level:.2f}", end="")
        
    # Create and start the microphone array
    mic_array = MicrophoneArray(device_name="ReSpeaker")
    mic_array.add_audio_callback(audio_handler)
    mic_array.start_capture()
    
    try:
        print("Capturing audio (press Ctrl+C to stop)...")
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nStopping...")
        
    finally:
        mic_array.stop_capture()
        print("\nAudio capture stopped.")
