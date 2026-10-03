# Heartbeat Radar Sensor

A non-contact heartbeat detection project using the Rd-03D 24 GHz radar sensor and Raspberry Pi 4.

## Overview

This project reads the radar's UART stream, extracts target motion/speed data, filters the chest motion signal, and estimates heart rate in beats per minute (BPM).

It is designed for a Raspberry Pi 4, but the core logic is portable and can be adapted to other Linux/Python environments.

## Features

- Reads serialized radar output from the Rd-03D module
- Parses target data in UART frames
- Tracks chest motion via speed signal
- Removes baseline drift and high-frequency noise
- Band-pass filters the heartbeat band
- Estimates BPM using FFT and peak detection
- Logs data to CSV
- Supports live plotting for debugging

## Hardware

- Raspberry Pi 4
- Rd-03D 24GHz radar sensor
- Stable 5V supply for the radar
- Common ground between radar and Pi
- Jumper wires

## Wiring

Radar to Pi:

- Radar 5V -> external 5V supply positive
- Radar GND -> Pi GND
- Radar TX -> Pi RX (GPIO15 / pin 10)
- Radar RX -> Pi TX (GPIO14 / pin 8)

Important: TX/RX are crossed.

See `WIRING.md` for a more detailed diagram.

## Project Layout

```text
heartbeat-radar-sensor/
├── README.md
├── WIRING.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── read_radar.py
│   ├── signal_processor.py
│   ├── heartbeat_detector.py
│   └── calibrate.py
├── docs/
│   ├── INSTALLATION.md
│   └── TROUBLESHOOTING.md
├── data/
│   ├── raw/
│   └── processed/
└── tests/
    ├── test_signal_processor.py
    └── test_heartbeat_detector.py
```

## Installation

```bash
sudo apt update
sudo apt install -y python3-pip python3-serial python3-scipy python3-numpy python3-matplotlib

cd ~
git clone https://github.com/XIIIcj/heartbeat-radar-sensor.git
cd heartbeat-radar-sensor
python3 -m pip install -r requirements.txt
```

## Quick Start

```bash
python3 src/read_radar.py
```

For heartbeat extraction:

```bash
python3 src/heartbeat_detector.py --plot
```

## Serial Port

The radar communicates at 256000 baud using UART TTL.

Common Raspberry Pi UART path:

```bash
/dev/ttyAMA0
```

If your system exposes a different port, adjust `port` in the detector.

## Heartbeat Detection Method

The implemented algorithm uses a robust pipeline:

1. Read speed data from the radar frames
2. Buffer samples over a 20-60 second window
3. Remove DC offset and slow drift by detrending
4. Band-pass filter between 0.8 Hz and 3.0 Hz
5. Estimate dominant frequency via FFT
6. Convert frequency to BPM using: BPM = frequency * 60
7. Smooth output using moving average for stability
8. Use peak detection for validation and better robustness

This targets the usual human heartbeat range of roughly 48 to 180 BPM.

## Safety and Notes

This is a research/hobby project and is not intended for medical diagnosis.

## License

MIT
