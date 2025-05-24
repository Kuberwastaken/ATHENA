#!/usr/bin/env python3
"""
ATHENA Voice Assistant

Main application entry point for the ATHENA voice assistant system.
"""

import os
import sys
import argparse
import logging
import signal
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('athena.log')
    ]
)
logger = logging.getLogger("main")

def signal_handler(sig, frame):
    """Handle termination signals gracefully."""
    logger.info("Received termination signal")
    if 'assistant' in globals():
        logger.info("Stopping assistant...")
        assistant.stop()
    sys.exit(0)

def setup_signal_handlers():
    """Set up signal handlers for graceful termination."""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="ATHENA Voice Assistant")
    
    parser.add_argument(
        "--config", 
        type=str, 
        default="config.json",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--log-level", 
        type=str, 
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level"
    )
    
    parser.add_argument(
        "--no-hardware", 
        action="store_true",
        help="Run without hardware components (for development)"
    )
    
    return parser.parse_args()

def setup_logging(log_level):
    """Configure logging based on the specified level."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    logging.getLogger().setLevel(numeric_level)
    logger.info(f"Log level set to {log_level}")

def find_project_root():
    """Find the project root directory."""
    # Start with the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Traverse up until we find a directory containing both 'software' and 'hardware'
    while current_dir != os.path.dirname(current_dir):  # Stop at filesystem root
        if os.path.isdir(os.path.join(current_dir, 'software')) and \
           os.path.isdir(os.path.join(current_dir, 'hardware')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    
    # If we couldn't find it, use the script directory as fallback
    logger.warning("Could not find project root. Using script directory.")
    return os.path.dirname(os.path.abspath(__file__))

def add_project_paths():
    """Add project paths to sys.path."""
    project_root = find_project_root()
    logger.info(f"Project root: {project_root}")
    
    # Add the project root to the path if it's not already there
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
    # Add other important directories
    for dir_name in ['software', 'docs']:
        dir_path = os.path.join(project_root, dir_name)
        if dir_path not in sys.path and os.path.isdir(dir_path):
            sys.path.insert(0, dir_path)

def main():
    """Main application entry point."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up logging
    setup_logging(args.log_level)
    
    # Set up signal handlers
    setup_signal_handlers()
    
    # Add project directories to path
    add_project_paths()
    
    # Import assistant module (after paths are set)
    try:
        from software.core.assistant import Assistant
        
        # Create assistant instance
        logger.info("Creating ATHENA assistant")
        global assistant
        assistant = Assistant(config_path=args.config)
        
        # Start assistant
        logger.info("Starting ATHENA assistant")
        if assistant.start():
            logger.info("ATHENA assistant started successfully")
            
            # Keep the main thread alive
            while True:
                time.sleep(1)
                
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error in main application: {e}", exc_info=True)
    finally:
        # Make sure we stop the assistant
        if 'assistant' in globals():
            logger.info("Stopping assistant...")
            assistant.stop()
        
        logger.info("ATHENA application terminated")

if __name__ == "__main__":
    main()
