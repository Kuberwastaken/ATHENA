# Software Installation Guide

This guide will help you set up the ATHENA voice assistant software on your Raspberry Pi or development machine.

## Prerequisites

### Hardware Setup
- Raspberry Pi 4 (8GB recommended) with microSD card (64GB+)
- ReSpeaker 6-Mic Array (or compatible microphone)
- MicroSD card reader
- Network connection (Ethernet or Wi-Fi)

### Development Machine
- Windows, macOS, or Linux computer
- Python 3.10 or newer
- Git for version control
- SSH client for remote access

## Raspberry Pi Setup

### 1. Prepare the Operating System

**Download Raspberry Pi OS**
- Download Raspberry Pi OS Lite (64-bit) from [rpi.org](https://www.raspberrypi.org/software/)
- Use Raspberry Pi Imager to flash the OS to your microSD card

**Enable SSH and Configure Wi-Fi**
1. Mount the SD card on your computer
2. Create empty file named `ssh` in the boot partition
3. Create `wpa_supplicant.conf` for Wi-Fi setup:
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YOUR_WIFI_NETWORK"
    psk="YOUR_WIFI_PASSWORD"
}
```

### 2. Initial System Setup

**Boot and Connect**
1. Insert SD card into Raspberry Pi and boot
2. Find the Pi's IP address (check your router or use `nmap`)
3. SSH into the Pi: `ssh pi@YOUR_PI_IP`
4. Default password is `raspberry` - change it immediately!

**Update the System**
```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

**Install Required System Packages**
```bash
sudo apt install -y \
    python3-pip \
    python3-venv \
    git \
    portaudio19-dev \
    libffi-dev \
    libssl-dev \
    libasound2-dev \
    libsndfile1 \
    ffmpeg
```

### 3. Audio System Configuration

**Enable I2S for ReSpeaker**
```bash
# Add to /boot/config.txt
echo "dtparam=i2s=on" | sudo tee -a /boot/config.txt
echo "dtoverlay=i2s-mmap" | sudo tee -a /boot/config.txt
```

**Install ReSpeaker Drivers**
```bash
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh
sudo reboot
```

**Test Audio Setup**
```bash
# List audio devices
arecord -l
aplay -l

# Test recording (should show ReSpeaker device)
arecord -D plughw:CARD=seeed8micvoicec,DEV=0 -c 8 -r 16000 -f S16_LE test.wav
```

## ATHENA Software Installation

### 1. Clone the Repository

```bash
cd /home/pi
git clone https://github.com/YOUR_USERNAME/PROJECT-ATHENA.git
cd PROJECT-ATHENA/ATHENA
```

### 2. Create Python Virtual Environment

```bash
python3 -m venv athena-env
source athena-env/bin/activate
```

**Add to ~/.bashrc for automatic activation:**
```bash
echo "source /home/pi/PROJECT-ATHENA/ATHENA/athena-env/bin/activate" >> ~/.bashrc
```

### 3. Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install PyTorch (CPU version for Raspberry Pi)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other requirements
pip install -r requirements.txt
```

### 4. Hardware Permissions Setup

**GPIO Access**
```bash
# Add user to gpio group
sudo usermod -a -G gpio pi

# For LED control (if using WS281X LEDs)
sudo pip install rpi_ws281x
```

**Audio Permissions**
```bash
# Add user to audio group
sudo usermod -a -G audio pi
```

### 5. Configuration

**Copy and Edit Configuration**
```bash
cp config.json config.local.json
nano config.local.json
```

**Update key settings:**
```json
{
    "audio": {
        "device_name": "seeed8micvoicec",
        "sample_rate": 16000,
        "channels": 6
    },
    "hardware": {
        "led_enabled": true,
        "led_gpio_pin": 18
    }
}
```

## Development Environment Setup

### 1. Local Development (Windows/macOS/Linux)

**Install Python and Dependencies**
```bash
# Create virtual environment
python -m venv athena-dev-env
source athena-dev-env/bin/activate  # Linux/macOS
# or
athena-dev-env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

**Run in Development Mode**
```bash
python main.py --no-hardware --log-level DEBUG
```

### 2. VS Code Setup (Recommended)

**Install Extensions**
- Python
- Remote - SSH
- GitLens

**Remote Development**
1. Install "Remote - SSH" extension
2. Connect to Pi: `ssh pi@YOUR_PI_IP`
3. Open project folder: `/home/pi/PROJECT-ATHENA/ATHENA`

## Testing the Installation

### 1. Basic Functionality Test

```bash
# Test main application
python main.py --help

# Test with development mode (no hardware required)
python main.py --no-hardware --log-level INFO
```

### 2. Hardware Tests

**LED Test**
```bash
# Test LED functionality (requires hardware)
python -c "
from software.hardware.led import LEDController
led = LEDController(simulation=False)
led.solid_color((255, 0, 0))  # Red
"
```

**Microphone Test**
```bash
# Test microphone input
python -c "
from software.audio.microphone import MicrophoneArray
mic = MicrophoneArray(device_name='seeed8micvoicec')
mic.start_capture()
print('Recording for 5 seconds...')
import time; time.sleep(5)
mic.stop_capture()
print('Test complete')
"
```

## Service Setup (Production)

### 1. Create Systemd Service

**Create service file:**
```bash
sudo nano /etc/systemd/system/athena.service
```

**Service configuration:**
```ini
[Unit]
Description=ATHENA Voice Assistant
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/PROJECT-ATHENA/ATHENA
Environment=PATH=/home/pi/PROJECT-ATHENA/ATHENA/athena-env/bin
ExecStart=/home/pi/PROJECT-ATHENA/ATHENA/athena-env/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
sudo systemctl enable athena.service
sudo systemctl start athena.service
sudo systemctl status athena.service
```

### 2. Log Management

**View logs:**
```bash
# Real-time logs
sudo journalctl -u athena.service -f

# Application logs
tail -f /home/pi/PROJECT-ATHENA/ATHENA/athena.log
```

## Troubleshooting

### Common Issues

**Audio Device Not Found**
```bash
# Check available devices
arecord -l
# Update device name in config.json
```

**Permission Denied for GPIO**
```bash
# Add user to gpio group
sudo usermod -a -G gpio pi
# Logout and login again
```

**Python Module Import Errors**
```bash
# Ensure virtual environment is activated
source athena-env/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```

**Memory Issues on Raspberry Pi**
```bash
# Increase swap space
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile  # Change CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Getting Help

1. Check the logs: `tail -f athena.log`
2. Run with debug logging: `python main.py --log-level DEBUG`
3. Check [Troubleshooting Guide](user-guides/troubleshooting.md)
4. Submit issues on GitHub

## Next Steps

After successful installation:

1. Read the [Basic Operation Guide](user-guides/basic-operation.md)
2. Configure your [Voice Commands](user-guides/voice-commands.md)
3. Explore [Configuration Options](user-guides/configuration.md)
4. Consider [Contributing](../CONTRIBUTING.md) to the project

---

*Last updated: May 24, 2025*
