# Audio Processing

This directory contains the audio processing components for the ATHENA voice assistant.

## Components

- `microphone.py`: Interface with the ReSpeaker microphone array
- `wake_word/`: Wake word detection system
- `noise_reduction/`: Noise reduction and audio preprocessing
- `playback.py`: Audio output and speaker management
- `vad.py`: Voice activity detection

## Microphone Array

The microphone array interface handles:

- Raw audio capture from the ReSpeaker 6-mic array
- Audio stream management
- Beamforming for directional audio capture
- Channel selection and mixing

## Wake Word Detection

The wake word detection system:

- Uses a lightweight model for local processing
- Operates continuously on the audio stream
- Has minimal false positives/negatives
- Supports custom wake words
- Uses DoA (Direction of Arrival) estimation

## Voice Activity Detection (VAD)

The VAD system:

- Detects when someone is speaking
- Helps determine when a command has ended
- Reduces processing overhead by only analyzing relevant audio

## Noise Reduction

Audio preprocessing includes:

- Acoustic echo cancellation
- Background noise reduction
- Signal normalization
- Frequency filtering

## Audio Playback

The playback system handles:

- Audio output management
- Volume control
- Ducking (lowering volume during listen mode)
- Audio format conversion

## Dependencies

- PyAudio
- NumPy
- librosa
- webrtcvad
- PyTorch (for wake word models)

## Development Status

This is a work in progress. Current focus is on:

- Microphone array integration
- Wake word detection reliability
- Basic audio preprocessing

*Code will be added as it is developed.*
