# Troubleshooting

## No data from the radar

- Check the 5V power supply
- Confirm common ground between Pi and radar
- Confirm TX/RX are crossed
- Check serial port path
- Check baud rate is 256000

## Unstable readings

- Use a separate regulated 5V supply for the radar
- Reduce nearby motion and vibration
- Keep the subject still and within 15-30 cm
- Run `python3 src/calibrate.py`

## Bad BPM values

- Increase the buffer length
- Tune the bandpass range
- Keep the target in a fixed position
- Avoid reflective metal surfaces nearby

## Serial permission errors

```bash
sudo usermod -a -G dialout $USER
```

Then log out and back in.
