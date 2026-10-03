# Raspberry Pi 4 Wiring Diagram

## Connections

```
                 Raspberry Pi 4
          +----------------------------------+
          |                                  |
  5V --|-----> external 5V supply +  ---->|  radar 5V
          |
  GND --|------------------------------>|  radar GND
          |
  Pi RX (GPIO15, pin 10) <-----------|  radar TX
          |
  Pi TX (GPIO14, pin 8) ------------>|  radar RX
          |
          +----------------------------------+
```

## UART Pin Reference

- Pi TX (GPIO14) = physical pin 8
- Pi RX (GPIO15) = physical pin 10
- Pi GND = any ground pin, e.g. pin 6

## Important Notes

- Use a regulated 5V source for the radar.
- The radar draws roughly 110 mA on average.
- Always share ground between Pi and radar.
- TX and RX must be crossed.

## Example Cable Map

| Radar Signal | Raspberry Pi |
|--------------|--------------|
| 5V           | 5V power source |
| GND          | GND |
| TX           | RX (GPIO15 / pin 10) |
| RX           | TX (GPIO14 / pin 8) |

## Optional USB-TTL Adapter

If you prefer not to use the Pi's UART directly, you can also connect the radar to a USB-TTL adapter and read it from a serial port such as `/dev/ttyUSB0`.
