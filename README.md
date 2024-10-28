# Musik Plair

Hands-Free Music Control: Play, Pause, and Move to the Beat!

## Introduction
Musik Plair is a motion-activated music player built with Python, Arduino, and a PIR (Passive Infrared) sensor. The system automatically toggles music playback based on detected motion, providing an interactive, hands-free audio experience.

## Features
- **Motion-Activated Control**: Music playback automatically starts or stops based on detected motion.
- **Sleek GUI**: Built with `customtkinter` for an intuitive, user-friendly interface.
- **MP3 Playback with `pygame`**: Supports playback of MP3 files with album art display and a dynamic progress bar.
- **Real-Time Serial Communication**: Integrates with Arduino’s PIR sensor for real-time motion data using `pyserial`.
- **Data Logging with RTC**: Logs motion events with timestamps, ideal for tracking usage patterns or security.

## Components
1. **Arduino with PIR Sensor**: Detects motion and communicates with Python via serial data.
2. **Python Music Player Interface**: Uses `pygame` for MP3 playback and `customtkinter` for GUI design.
3. **Data Logger Shield with RTC**: Logs motion events with timestamps for monitoring.

## Tech Stack
- **Python**: GUI, audio playback, and serial communication.
- **Arduino**: PIR sensor data collection and RTC data logging.
- **Libraries**: `pygame`, `mutagen`, `pyserial`, `customtkinter`, `Pillow`.

 Connect Arduino with PIR sensor to your system and upload the provided Arduino code.

## Usage
1. Run the `Musik Plair` Python script.
2. Select an MP3 file from the GUI.
3. Motion detected by the PIR sensor will toggle playback automatically.

## Contributing
Pull requests are welcome. For major changes, please open an issue to discuss what you would like to change.
