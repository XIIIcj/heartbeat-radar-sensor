# Installation Guide

## 1) Install Raspberry Pi OS

Install Raspberry Pi OS Lite or Desktop on your Pi 4.

## 2) Update the OS

```bash
sudo apt update
sudo apt upgrade -y
```

## 3) Install Python dependencies

```bash
sudo apt install -y python3-pip python3-serial python3-scipy python3-numpy python3-matplotlib
```

## 4) Verify the serial port

```bash
ls /dev/serial*
```

Typical output may include one of:

- `/dev/ttyAMA0`
- `/dev/ttyS0`
- `/dev/ttyUSB0`

## 5) Enable UART if necessary

```bash
sudo raspi-config
```

Navigate to:

- Interface Options
- Serial Port
- Disable login shell over serial
- Enable serial hardware

Then reboot.

## 6) Clone Repo

```bash
git clone https://github.com/XIIIcj/heartbeat-radar-sensor.git
cd heartbeat-radar-sensor
python3 -m pip install -r requirements.txt
```

## 7) Test the radar

```bash
python3 src/read_radar.py
```

## 8) Run heartbeat detector

```bash
python3 src/heartbeat_detector.py --plot
```

If you get no output, check the wiring and power supply.
