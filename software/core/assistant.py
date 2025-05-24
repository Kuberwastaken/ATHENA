"""
Core Assistant Module for Project ATHENA

This is the main assistant module that coordinates all functionality
of the ATHENA voice assistant system.
"""

import logging
import threading
import time
import json
import os
from enum import Enum

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("assistant")

class AssistantState(Enum):
    """Enum representing the different states of the assistant."""
    IDLE = 0
    LISTENING = 1
    PROCESSING = 2
    RESPONDING = 3
    ERROR = 4

class Assistant:
    """
    Core assistant class that manages all ATHENA functionality.
    
    This class serves as the central coordinator for the voice assistant,
    managing the interactions between various components like wake word detection,
    speech recognition, natural language processing, and skill execution.
    """
    
    def __init__(self, config_path=None):
        """
        Initialize the assistant.
        
        Args:
            config_path: Path to the configuration file
        """
        self.state = AssistantState.IDLE
        self.config = self._load_config(config_path)
        self.components = {}
        self.skills = {}
        self.listeners = []
        
        logger.info("Initializing ATHENA assistant")
    
    def _load_config(self, config_path):
        """
        Load the configuration from a file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            dict: Loaded configuration
        """
        default_config = {
            "name": "ATHENA",
            "wake_word": "athena",
            "voice": {
                "language": "en-US",
                "voice_id": "en-US-Standard-C",
                "speaking_rate": 1.0,
                "pitch": 0.0
            },
            "audio": {
                "sample_rate": 16000,
                "channels": 6,
                "device_name": "ReSpeaker"
            },
            "speech_recognition": {
                "use_cloud": False,
                "timeout": 10.0
            },
            "skills": {
                "enabled": ["system", "time", "weather"]
            },
            "hardware": {
                "led_enabled": True,
                "display_enabled": False
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # Merge with default config
                    for key, value in config.items():
                        if isinstance(value, dict) and key in default_config:
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
                logger.info(f"Configuration loaded from {config_path}")
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
                logger.info("Using default configuration")
        else:
            logger.info("No configuration file found, using default configuration")
            
        return default_config
    
    def start(self):
        """Start the assistant and all its components."""
        logger.info("Starting ATHENA assistant")
        
        try:
            # Initialize and start components
            self._init_components()
            
            # Load skills
            self._load_skills()
            
            # Set initial state
            self._set_state(AssistantState.IDLE)
            
            logger.info("ATHENA assistant started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting assistant: {e}")
            self._set_state(AssistantState.ERROR)
            return False
    
    def stop(self):
        """Stop the assistant and all its components."""
        logger.info("Stopping ATHENA assistant")
        
        # Stop all components
        for name, component in self.components.items():
            if hasattr(component, 'stop'):
                try:
                    component.stop()
                    logger.info(f"Component '{name}' stopped")
                except Exception as e:
                    logger.error(f"Error stopping component '{name}': {e}")
        
        # Clear components and skills
        self.components = {}
        self.skills = {}
        
        # Set state to IDLE
        self._set_state(AssistantState.IDLE)
        
        logger.info("ATHENA assistant stopped")
    
    def _init_components(self):
        """Initialize all assistant components."""
        try:
            # Here we would initialize:
            # 1. Microphone Array
            # 2. Wake Word Detector
            # 3. Speech Recognition
            # 4. Natural Language Processing
            # 5. Text-to-Speech
            # 6. Hardware Interfaces (LED, Display, Buttons)
            
            # This is a placeholder for the actual component initialization
            logger.info("Initializing assistant components")
            
            # Import here to avoid circular imports
            from software.audio.microphone import MicrophoneArray
            from software.audio.wake_word import WakeWordDetector
            
            # Initialize microphone array
            mic_config = self.config["audio"]
            mic_array = MicrophoneArray(
                device_name=mic_config.get("device_name"),
                sample_rate=mic_config.get("sample_rate", 16000),
                channels=mic_config.get("channels", 6)
            )
            self.components["microphone"] = mic_array
            
            # Initialize wake word detector
            wake_word_detector = WakeWordDetector(
                trigger_threshold=0.8,
                sample_rate=mic_config.get("sample_rate", 16000)
            )
            self.components["wake_word"] = wake_word_detector
            
            # Set up audio pipeline
            # Connect wake word detector to microphone
            mic_array.add_audio_callback(lambda mono_audio, _: wake_word_detector.process_audio(mono_audio))
            
            # Set up wake word callback
            wake_word_detector.start(detection_callback=self._on_wake_word_detected)
            
            # Start microphone capture
            mic_array.start_capture()
            
            logger.info("Assistant components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
    
    def _load_skills(self):
        """Load all enabled skills."""
        try:
            enabled_skills = self.config.get("skills", {}).get("enabled", [])
            logger.info(f"Loading skills: {enabled_skills}")
            
            # This is a placeholder for actual skill loading
            # In a real implementation, we would dynamically load skill modules
            
            for skill_name in enabled_skills:
                logger.info(f"Loading skill: {skill_name}")
                # Placeholder for actual skill loading
                self.skills[skill_name] = {"name": skill_name, "loaded": True}
            
            logger.info(f"Loaded {len(self.skills)} skills")
            
        except Exception as e:
            logger.error(f"Error loading skills: {e}")
            raise
    
    def _on_wake_word_detected(self, confidence):
        """
        Handle wake word detection event.
        
        Args:
            confidence: Detection confidence score
        """
        logger.info(f"Wake word detected with confidence: {confidence:.2f}")
        
        # Change state to LISTENING
        self._set_state(AssistantState.LISTENING)
        
        # In a real implementation, we would:
        # 1. Play a sound to indicate we're listening
        # 2. Start capturing the user's speech
        # 3. Send the speech to the recognition engine
        # 4. Process the command
        
        # For now, we'll just simulate this process
        threading.Thread(target=self._simulate_interaction).start()
    
    def _simulate_interaction(self):
        """Simulate a user interaction for demonstration purposes."""
        # Simulate listening for 2 seconds
        time.sleep(2)
        
        # Simulate processing
        self._set_state(AssistantState.PROCESSING)
        time.sleep(1)
        
        # Simulate responding
        self._set_state(AssistantState.RESPONDING)
        time.sleep(2)
        
        # Return to idle
        self._set_state(AssistantState.IDLE)
    
    def _set_state(self, new_state):
        """
        Set the assistant state and notify listeners.
        
        Args:
            new_state: New AssistantState value
        """
        old_state = self.state
        self.state = new_state
        
        # Notify state change listeners
        for listener in self.listeners:
            listener(old_state, new_state)
        
        logger.info(f"Assistant state changed: {old_state.name} -> {new_state.name}")
    
    def add_state_listener(self, listener):
        """
        Add a state change listener function.
        
        Args:
            listener: Function that accepts old_state and new_state parameters
        """
        if listener not in self.listeners:
            self.listeners.append(listener)
    
    def remove_state_listener(self, listener):
        """Remove a previously added state listener function."""
        if listener in self.listeners:
            self.listeners.remove(listener)
    
    def get_state(self):
        """Get the current assistant state."""
        return self.state


# Example usage
if __name__ == "__main__":
    def state_change_handler(old_state, new_state):
        print(f"Assistant state changed: {old_state.name} -> {new_state.name}")
    
    # Create and start the assistant
    assistant = Assistant()
    assistant.add_state_listener(state_change_handler)
    
    if assistant.start():
        try:
            print("ATHENA assistant is running (press Ctrl+C to stop)...")
            while True:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nStopping...")
            
        finally:
            assistant.stop()
            print("ATHENA assistant stopped.")
