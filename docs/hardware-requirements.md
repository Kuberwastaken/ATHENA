# Hardware Requirements

## Minimum System Requirements

### Processing Unit
- **Raspberry Pi 4 Model B (8GB RAM)** - Required
  - Quad-core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5GHz
  - 8GB LPDDR4-3200 SDRAM (4GB may work but not recommended)
  - microSD card (64GB Class 10 or better recommended)
  - USB-C power supply (5V/3A minimum)

### Audio Input
- **ReSpeaker 6-Mic Circular Array Kit** (Recommended)
  - 6 high-performance digital microphones
  - Built-in DSP for audio preprocessing
  - Compatible with Raspberry Pi GPIO
  - Alternative: Any USB microphone array with 4+ channels

### Audio Output
- **Custom Speaker System** (Planned)
  - 3-inch mid-range driver (4-8 ohms, 10-20W)
  - 1-inch tweeter (optional, for enhanced high frequencies)
  - Audio amplifier (Class D, 20W+ per channel)
- **Alternative**: Any powered speakers with 3.5mm input

### Visual Feedback
- **NeoPixel LED Ring** (Recommended)
  - 24 individually addressable RGB LEDs
  - WS2812B compatible
  - 5V power supply compatible
- **Optional Display**
  - SSD1306 OLED (128x64) or similar
  - I2C interface preferred

## Custom Hardware Components

### Power Management PCB (In Development)
- **Input**: 12V DC barrel jack
- **Outputs**: 
  - 5V/3A for Raspberry Pi
  - 5V/2A for audio amplifier
  - 3.3V for microcontroller circuits
- **Features**:
  - Overcurrent protection
  - Clean power filtering
  - Status LEDs

### Audio Amplifier PCB (In Development)
- **Amplifier IC**: TPA3116D2 or similar Class D
- **Power**: 20W per channel @ 4 ohms
- **Features**:
  - Volume control
  - Mute control
  - Thermal protection
  - Low EMI design

## Mechanical Components

### Enclosure (Custom Design)
- **Material**: PLA+ or PETG for 3D printing
- **Design**: Cylindrical form factor
- **Features**:
  - Acoustic ports for speaker
  - Microphone openings
  - LED diffuser ring
  - Ventilation for Raspberry Pi
  - Access panels for connections

### Hardware
- **Fasteners**: M3 screws and standoffs
- **Cables**: Custom length interconnects
- **Damping**: Acoustic foam for speaker cavity

## Connectivity

### Required Connections
- **Power**: 12V DC input
- **Network**: Ethernet or Wi-Fi (Pi 4 built-in)
- **USB**: For development and updates

### Optional Connections
- **HDMI**: For setup and debugging
- **GPIO**: Expansion connector for future modules
- **Audio Out**: 3.5mm jack for external speakers during development

## Development Hardware

### Additional Components for Development
- **MicroSD Card Reader**: For flashing images
- **USB-C Cable**: For Raspberry Pi power during development
- **HDMI Cable**: For initial setup
- **USB Keyboard/Mouse**: For initial configuration
- **Breadboard & Jumper Wires**: For prototyping circuits

### Test Equipment (Optional)
- **Multimeter**: For voltage and continuity testing
- **Oscilloscope**: For audio signal analysis
- **Sound Level Meter**: For acoustic testing
- **Spectrum Analyzer**: For frequency response testing

## Performance Specifications

### Audio Specifications
- **Frequency Response**: 80Hz - 20kHz (target)
- **Signal-to-Noise Ratio**: >80dB
- **Total Harmonic Distortion**: <1% @ 1W
- **Maximum Output**: 20W peak

### Processing Requirements
- **Wake Word Detection**: <100ms latency
- **Speech Recognition**: <500ms for local processing
- **Response Generation**: <2s for simple queries
- **Memory Usage**: <4GB during normal operation

## Cost Breakdown

| Category | Component | Cost (USD) |
|----------|-----------|------------|
| Computing | Raspberry Pi 4 8GB | $55 |
| Audio Input | ReSpeaker 6-Mic Array | $35 |
| Audio Output | Speaker Components | $45 |
| Electronics | Custom PCBs | $25 |
| Mechanical | 3D Printed Case | $15 |
| Mechanical | Laser Cut Parts | $15 |
| Visual | LED Ring | $8 |
| Visual | Optional Display | $35 |
| Power | Power Supply | $12 |
| Power | Power Management | $8 |
| Misc | Connectors, Hardware | $15 |
| **Total** | | **$275** |

## Sourcing Information

### Primary Suppliers
- **Raspberry Pi**: Official distributors (Adafruit, SparkFun, etc.)
- **ReSpeaker**: Seeed Studio
- **LEDs**: Adafruit (NeoPixel products)
- **PCB Fabrication**: JLCPCB, PCBWay, or OSH Park
- **3D Printing**: Local service or personal printer

### International Considerations
- Component availability may vary by region
- Import duties and shipping costs not included in pricing
- Some components may require local electrical certifications

## Assembly Prerequisites

### Skills Required
- **Basic Electronics**: Soldering, wire management
- **3D Printing**: If printing case components
- **Software Setup**: Linux command line familiarity
- **Debugging**: Basic troubleshooting skills

### Tools Required
- **Soldering Iron**: Temperature controlled (recommended)
- **Multimeter**: For testing and debugging
- **Small Screwdrivers**: Phillips and flathead
- **Wire Strippers**: For cable preparation
- **Heat Shrink Tubing**: For wire connections

---

*Last updated: May 24, 2025*
