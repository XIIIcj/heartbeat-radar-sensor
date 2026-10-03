from __future__ import annotations

import serial
import struct


class RadarReader:
    def __init__(self, port: str = "/dev/ttyAMA0", baudrate: int = 256000):
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(port, baudrate, timeout=1)

    def read_frame(self):
        buffer = bytearray()
        while True:
            byte = self.serial.read(1)
            if not byte:
                continue
            buffer.extend(byte)
            if len(buffer) >= 32:
                if buffer[0] == 0xAA and buffer[1] == 0xFF:
                    frame = bytes(buffer[:32])
                    parsed = self._parse_frame(frame)
                    buffer = bytearray(buffer[32:])
                    return parsed
                buffer = bytearray(buffer[1:])

    def _parse_frame(self, frame: bytes):
        if len(frame) < 32:
            return None

        targets = []
        for i in range(3):
            offset = 4 + i * 8
            x = struct.unpack_from("<h", frame, offset)[0]
            y = struct.unpack_from("<h", frame, offset + 2)[0]
            speed = struct.unpack_from("<h", frame, offset + 4)[0]
            distance = struct.unpack_from("<H", frame, offset + 6)[0]
            if distance > 0:
                targets.append({
                    "x_mm": x,
                    "y_mm": y,
                    "speed_cm_s": speed,
                    "distance_mm": distance,
                })
        return targets

    def close(self):
        self.serial.close()


if __name__ == "__main__":
    reader = RadarReader()
    try:
        while True:
            frame = reader.read_frame()
            print(frame)
    except KeyboardInterrupt:
        reader.close()
        print("Stopped")
