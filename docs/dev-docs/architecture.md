# Architecture Overview

This document provides a comprehensive overview of the ATHENA voice assistant architecture, including software components, data flow, and system design principles.

## System Architecture

### High-Level Overview

ATHENA follows a modular, event-driven architecture designed for extensibility, maintainability, and performance. The system is built around a central coordinator (the Assistant) that manages interactions between various specialized components.

```
┌─────────────────────────────────────────────────────────────┐
│                    ATHENA Core System                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │    Web      │  │   Assistant  │  │   Skills        │    │
│  │  Interface  │◄─┤   (Core)     ├─►│   Framework     │    │
│  └─────────────┘  └──────┬───────┘  └─────────────────┘    │
│                          │                                  │
│  ┌─────────────┐  ┌──────┴───────┐  ┌─────────────────┐    │
│  │   Audio     │  │   Hardware   │  │   AI/ML         │    │
│  │ Processing  │◄─┤   Control    ├─►│   Pipeline      │    │
│  └─────────────┘  └──────────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

1. **Assistant Core**: Central coordinator and state manager
2. **Audio Processing**: Microphone input, wake word detection, audio output
3. **AI/ML Pipeline**: Speech recognition, NLP, text-to-speech
4. **Skills Framework**: Extensible plugin system for capabilities
5. **Hardware Control**: LED, display, button management
6. **Web Interface**: Configuration and control interface

## Component Architecture

### 1. Assistant Core (`software/core/assistant.py`)

The heart of the ATHENA system, responsible for:
- System state management
- Component lifecycle coordination
- Event routing and handling
- Configuration management

**Key Classes:**
```python
class Assistant:
    - _load_config()
    - start() / stop()
    - _initialize_components()
    - _handle_wake_word()
    - _process_speech()
    - _execute_skill()
```

**State Machine:**
```
IDLE ──────► LISTENING ──────► PROCESSING ──────► RESPONDING
 ▲                                                      │
 └──────────────────────────────────────────────────────┘
```

### 2. Audio Processing Pipeline

#### Microphone Array (`software/audio/microphone.py`)
- **Purpose**: Capture and preprocess audio from the 6-microphone array
- **Features**: 
  - Multi-channel audio capture
  - Real-time audio streaming
  - Noise reduction and filtering
  - Channel mixing and beamforming

**Key Methods:**
```python
class MicrophoneArray:
    - start_capture()
    - stop_capture()
    - get_audio_data()
    - apply_beamforming()
```

#### Wake Word Detection (`software/audio/wake_word.py`)
- **Purpose**: Continuously monitor audio for trigger phrases
- **Features**:
  - Low-latency detection
  - Configurable sensitivity
  - Multiple wake word support
  - False positive reduction

**Detection Pipeline:**
```
Audio Stream → Feature Extraction → Model Inference → Threshold Check → Event
```

### 3. AI/ML Pipeline

#### Speech Recognition
- **Technology**: OpenAI Whisper (local deployment)
- **Features**: Multilingual support, noise robustness, real-time processing
- **Models**: Configurable size (tiny/base/small/medium/large)

#### Natural Language Processing
- **Technology**: Local transformer models or cloud fallback
- **Features**: Intent recognition, entity extraction, context understanding
- **Privacy**: Configurable local-only processing

#### Text-to-Speech
- **Technology**: Piper TTS (planned)
- **Features**: Natural voice synthesis, configurable voices, low latency
- **Quality**: High-quality neural voices

### 4. Skills Framework (`software/skills/`)

Modular plugin system for extending ATHENA's capabilities.

**Base Skill Interface:**
```python
class BaseSkill:
    def can_handle(self, intent: Intent) -> bool
    def execute(self, intent: Intent) -> Response
    def get_examples(self) -> List[str]
```

**Skill Categories:**
- **System Skills**: Device control, settings, information
- **Information Skills**: Weather, time, calendar, knowledge
- **Entertainment Skills**: Music, jokes, games
- **Smart Home Skills**: IoT device control
- **Communication Skills**: Messages, calls, reminders

**Skill Loading:**
```
Scan Directories → Load Modules → Register Handlers → Route Requests
```

### 5. Hardware Control

#### LED Controller (`software/hardware/led.py`)
- **Purpose**: Visual feedback and status indication
- **Features**: Multiple effects, color patterns, brightness control
- **Hardware**: NeoPixel (WS2812B) LED ring/strip

**Effect Types:**
```python
class LEDEffect(Enum):
    SOLID = 0      # Static color
    PULSE = 1      # Breathing effect
    SPIN = 2       # Rotating pattern
    BREATHE = 3    # Smooth fade in/out
    RAINBOW = 4    # Color cycling
    PROGRESS = 5   # Progress indication
```

#### Display Interface (Planned)
- **Purpose**: Text and graphical information display
- **Hardware**: OLED/LCD displays
- **Content**: Status, time, responses, visualizations

#### Button Controls (Planned)
- **Purpose**: Physical user interaction
- **Features**: Volume, mute, action buttons
- **Debouncing**: Software debouncing for reliable input

### 6. Web Interface (`software/web/`)

Browser-based configuration and control interface.

**Features:**
- Real-time status monitoring
- Configuration management
- Skill management
- Audio level visualization
- System logs viewing

**Technology Stack:**
- **Backend**: FastAPI with WebSocket support
- **Frontend**: HTML/CSS/JavaScript with real-time updates
- **API**: RESTful endpoints for configuration

## Data Flow

### 1. Wake Word Detection Flow
```
Microphone → Audio Buffer → Feature Extraction → Model → Threshold → Event
     ↓              ↓              ↓               ↓          ↓
  6-channel    Circular       MFCC/Mel       CNN/RNN    Confidence
   16kHz      Buffer         Spectrogram      Model      > 0.8
```

### 2. Voice Command Processing Flow
```
Wake Word → Record Audio → Speech Recognition → NLP → Skill Routing → TTS → Audio Output
    ↓            ↓              ↓              ↓         ↓           ↓         ↓
 Detected    Fixed Duration   Whisper STT    Intent   Execute     Piper      Speaker
 "Athena"    or VAD Stop     Text Output    Match    Skill       TTS        Audio
```

### 3. Configuration Flow
```
Config File → JSON Parser → Validation → Component Init → Runtime Updates
     ↓            ↓           ↓             ↓               ↓
config.json   Parse Tree   Schema Check   Set Params    Hot Reload
```

## Design Principles

### 1. Modularity
- **Separation of Concerns**: Each component has a single responsibility
- **Loose Coupling**: Components communicate through well-defined interfaces
- **Plugin Architecture**: Skills and hardware drivers are pluggable

### 2. Privacy by Design
- **Local Processing**: All sensitive operations can run locally
- **Configurable Cloud**: Optional cloud services with explicit consent
- **Data Minimization**: Minimal data retention and processing
- **Transparency**: Open source for full auditability

### 3. Extensibility
- **Plugin System**: Easy addition of new skills and capabilities
- **Configuration Driven**: Behavior modification without code changes
- **API First**: All functionality accessible through APIs
- **Hardware Abstraction**: Support for different hardware configurations

### 4. Performance
- **Asynchronous Processing**: Non-blocking operations where possible
- **Resource Management**: Efficient use of Raspberry Pi resources
- **Caching**: Intelligent caching of models and data
- **Optimization**: Platform-specific optimizations

### 5. Reliability
- **Error Handling**: Graceful degradation on component failure
- **Logging**: Comprehensive logging for debugging
- **Recovery**: Automatic recovery from transient failures
- **Testing**: Comprehensive test coverage

## Development Architecture

### Code Organization
```
ATHENA/
├── main.py                 # Application entry point
├── config.json            # Configuration file
├── software/              # Core software components
│   ├── core/             # Central coordinator
│   ├── audio/            # Audio processing
│   ├── hardware/         # Hardware interfaces
│   ├── skills/           # Skills framework
│   ├── web/              # Web interface
│   └── tools/            # Utilities and tools
├── hardware/             # Hardware design files
├── docs/                 # Documentation
└── tests/                # Test suite
```

### Dependencies
- **Core**: Python 3.10+, PyTorch, Transformers
- **Audio**: PyAudio, SoundDevice, Librosa
- **Hardware**: RPi.GPIO, rpi-ws281x
- **Web**: FastAPI, WebSockets, Jinja2
- **AI/ML**: Whisper, Transformers, NumPy

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **Hardware Tests**: Real hardware validation
- **Performance Tests**: Latency and resource usage
- **End-to-End Tests**: Complete user scenarios

## Deployment Architecture

### Development Environment
- **Local Machine**: Full development with hardware simulation
- **Remote Debugging**: SSH-based development on Raspberry Pi
- **Container Support**: Docker for consistent environments

### Production Deployment
- **Raspberry Pi**: Primary target platform
- **Systemd Service**: Automatic startup and management
- **Log Management**: Structured logging with rotation
- **Update Mechanism**: Over-the-air updates

### Scaling Considerations
- **Single Device**: Optimized for single Raspberry Pi
- **Multi-Room**: Potential for networked devices
- **Cloud Hybrid**: Optional cloud processing for heavy tasks
- **Edge Computing**: Distributed processing capabilities

## Security Architecture

### Local Security
- **Process Isolation**: Sandboxed component execution
- **File Permissions**: Minimal required file access
- **Network Security**: Firewall configuration
- **Update Security**: Signed update packages

### Privacy Protection
- **Local Processing**: Keep sensitive data on device
- **Encryption**: Encrypted storage of sensitive data
- **Access Control**: Role-based access to functionality
- **Audit Logging**: Track all data access

---

*Last updated: May 24, 2025*
