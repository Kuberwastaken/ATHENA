# Core Assistant

This directory contains the core functionality of the ATHENA voice assistant.

## Components

- `assistant.py`: Main assistant class that coordinates all functionality
- `nlp/`: Natural language processing components
- `tts/`: Text-to-speech synthesis
- `stt/`: Speech-to-text processing
- `intent/`: Intent recognition and processing
- `dialog/`: Dialog management and context tracking

## Architecture

The core assistant operates using a modular architecture:

1. Audio input is processed through the audio pipeline
2. Speech is converted to text using the STT module
3. Text is analyzed by the NLP module for intent recognition
4. The intent handler dispatches to appropriate skill modules
5. Responses are generated and converted to speech
6. Audio output is sent to the speaker system

## Dependencies

- PyTorch
- Transformers
- Pydantic
- FastAPI (for web interfaces)

## Configuration

Configuration is stored in YAML format and includes:

- Model parameters
- Voice settings
- Service endpoints
- Default behaviors

## Development Status

This is a work in progress. Current focus is on:

- Basic intent recognition
- Core dialog management
- Local model integration

*Code will be added as it is developed.*
