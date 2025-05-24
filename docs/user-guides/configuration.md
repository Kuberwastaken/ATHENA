# Configuration Options

ATHENA uses a JSON-based configuration system that allows extensive customization of the voice assistant's behavior and hardware settings.

## Configuration File Location

The main configuration file is `config.json` in the root directory. For local development or custom deployments, you can create a `config.local.json` file that will override the default settings.

## Core Configuration Structure

### Basic Settings

```json
{
    "name": "ATHENA",
    "wake_word": "athena",
    "voice": {
        "language": "en-US",
        "voice_id": "en-US-Standard-C",
        "speaking_rate": 1.0,
        "pitch": 0.0
    }
}
```

**Parameters:**
- `name`: Display name for the assistant
- `wake_word`: Trigger phrase to activate the assistant (default: "athena")
- `voice.language`: Language code for speech recognition and synthesis
- `voice.voice_id`: Specific voice model identifier for TTS
- `voice.speaking_rate`: Speed of speech (0.25 to 4.0, default: 1.0)
- `voice.pitch`: Voice pitch adjustment (-20.0 to 20.0, default: 0.0)

## Audio Configuration

### Input Settings

```json
{
    "audio": {
        "sample_rate": 16000,
        "channels": 6,
        "device_name": "ReSpeaker",
        "chunk_size": 1024,
        "gain": 1.0
    }
}
```

**Parameters:**
- `sample_rate`: Audio sampling rate in Hz (8000, 16000, 44100, 48000)
- `channels`: Number of microphone channels (1-8)
- `device_name`: Audio input device name or partial name
- `chunk_size`: Audio buffer size in samples (512, 1024, 2048)
- `gain`: Input gain multiplier (0.1 to 10.0)

### Speech Recognition

```json
{
    "speech_recognition": {
        "use_cloud": false,
        "timeout": 10.0,
        "language": "en-US",
        "model_size": "base",
        "energy_threshold": 300,
        "dynamic_energy_threshold": true
    }
}
```

**Parameters:**
- `use_cloud`: Enable cloud-based speech recognition fallback
- `timeout`: Maximum listening time in seconds
- `language`: Language code for recognition
- `model_size`: Whisper model size (tiny, base, small, medium, large)
- `energy_threshold`: Microphone sensitivity threshold
- `dynamic_energy_threshold`: Auto-adjust threshold based on ambient noise

## Hardware Configuration

### LED System

```json
{
    "hardware": {
        "led_enabled": true,
        "led_count": 24,
        "led_gpio_pin": 18,
        "led_brightness": 0.5,
        "led_frequency": 800000,
        "led_invert": false
    }
}
```

**Parameters:**
- `led_enabled`: Enable/disable LED feedback system
- `led_count`: Number of LEDs in the ring/strip (12, 16, 24, 60)
- `led_gpio_pin`: GPIO pin number for LED data (18, 12, 21)
- `led_brightness`: Global brightness (0.0 to 1.0)
- `led_frequency`: PWM frequency for LED control
- `led_invert`: Invert the LED signal

### Display Settings

```json
{
    "hardware": {
        "display_enabled": true,
        "display_type": "ssd1306",
        "display_width": 128,
        "display_height": 64,
        "display_i2c_address": "0x3C"
    }
}
```

**Parameters:**
- `display_enabled`: Enable/disable information display
- `display_type`: Display driver type (ssd1306, st7735, etc.)
- `display_width`: Display width in pixels
- `display_height`: Display height in pixels
- `display_i2c_address`: I2C address for display communication

### Button Controls

```json
{
    "hardware": {
        "buttons_enabled": true,
        "button_pins": {
            "mute": 21,
            "volume_up": 20,
            "volume_down": 16,
            "action": 26
        },
        "button_pull_up": true
    }
}
```

## Skills Configuration

### Enabled Skills

```json
{
    "skills": {
        "enabled": ["system", "time", "weather", "knowledge", "music"],
        "paths": ["software/skills"],
        "timeout": 30.0
    }
}
```

**Parameters:**
- `enabled`: List of skill names to load at startup
- `paths`: Directories to search for skill modules
- `timeout`: Maximum time for skill execution

### Individual Skill Settings

```json
{
    "skills": {
        "weather": {
            "default_location": "New York, NY",
            "units": "imperial",
            "api_key": "your_api_key_here"
        },
        "music": {
            "default_service": "spotify",
            "volume": 0.7
        }
    }
}
```

## API Integration

### External Services

```json
{
    "api": {
        "weather": {
            "provider": "openweathermap",
            "api_key": "YOUR_API_KEY_HERE",
            "units": "imperial"
        },
        "knowledge": {
            "provider": "wikipedia",
            "language": "en"
        }
    }
}
```

## Web Interface

### Server Settings

```json
{
    "web": {
        "enabled": true,
        "port": 8080,
        "host": "0.0.0.0",
        "debug": false,
        "auto_reload": false
    }
}
```

**Parameters:**
- `enabled`: Enable web interface
- `port`: HTTP port number (1024-65535)
- `host`: Bind address (0.0.0.0 for all interfaces, 127.0.0.1 for localhost only)
- `debug`: Enable debug mode (development only)
- `auto_reload`: Auto-reload on code changes (development only)

## System Configuration

### Localization

```json
{
    "system": {
        "language": "en-US",
        "units": "imperial",
        "time_format": "12h",
        "date_format": "MM/DD/YYYY",
        "timezone": "America/New_York"
    }
}
```

**Parameters:**
- `language`: System language code
- `units`: Measurement units (imperial, metric)
- `time_format`: Time display format (12h, 24h)
- `date_format`: Date display format
- `timezone`: System timezone

### Logging

```json
{
    "logging": {
        "level": "INFO",
        "file": "athena.log",
        "max_size": "10MB",
        "backup_count": 5,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
}
```

## Privacy Settings

### Data Handling

```json
{
    "privacy": {
        "always_ask_before_cloud": true,
        "audio_retention_days": 0,
        "allow_analytics": false,
        "anonymize_logs": true,
        "local_processing_only": false
    }
}
```

**Parameters:**
- `always_ask_before_cloud`: Prompt before using cloud services
- `audio_retention_days`: Days to keep audio recordings (0 = don't save)
- `allow_analytics`: Send anonymous usage data
- `anonymize_logs`: Remove personal information from logs
- `local_processing_only`: Disable all cloud services

## Advanced Configuration

### Performance Tuning

```json
{
    "performance": {
        "max_workers": 4,
        "audio_buffer_size": 4096,
        "processing_timeout": 30.0,
        "memory_limit": "2GB",
        "cpu_priority": "normal"
    }
}
```

### Debug Settings

```json
{
    "debug": {
        "save_audio": false,
        "audio_output_dir": "/tmp/athena_audio",
        "verbose_logging": false,
        "profile_performance": false
    }
}
```

## Environment Variables

Some settings can be overridden using environment variables:

```bash
export ATHENA_CONFIG_PATH="/path/to/custom/config.json"
export ATHENA_LOG_LEVEL="DEBUG"
export ATHENA_NO_HARDWARE="true"
export ATHENA_API_KEY_WEATHER="your_api_key"
```

## Configuration Validation

The system validates configuration on startup. Common validation errors:

- **Invalid JSON syntax**: Check for missing commas, brackets
- **Unknown parameters**: Typos in parameter names
- **Invalid values**: Out-of-range numbers, invalid enum values
- **Missing required fields**: Essential parameters not specified

## Example Configurations

### Development Setup
```json
{
    "name": "ATHENA-DEV",
    "hardware": {
        "led_enabled": false,
        "display_enabled": false,
        "buttons_enabled": false
    },
    "web": {
        "debug": true,
        "auto_reload": true
    },
    "logging": {
        "level": "DEBUG"
    }
}
```

### Production Setup
```json
{
    "name": "ATHENA",
    "privacy": {
        "local_processing_only": true,
        "audio_retention_days": 0
    },
    "performance": {
        "max_workers": 2,
        "memory_limit": "1GB"
    },
    "logging": {
        "level": "INFO",
        "anonymize_logs": true
    }
}
```

### Minimal Setup
```json
{
    "name": "ATHENA-MINIMAL",
    "skills": {
        "enabled": ["time", "system"]
    },
    "hardware": {
        "led_enabled": false,
        "display_enabled": false
    },
    "web": {
        "enabled": false
    }
}
```

## Configuration Management

### Command Line Overrides

```bash
# Use custom config file
python main.py --config custom_config.json

# Override log level
python main.py --log-level DEBUG

# Development mode (disables hardware)
python main.py --no-hardware
```

### Runtime Configuration Changes

Some settings can be changed at runtime through the web interface or API calls. These changes are temporary and don't modify the configuration file.

---

*Last updated: May 24, 2025*
