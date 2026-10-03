import argparse
import csv
import os
import time

import numpy as np

from src.signal_processor import SignalProcessor


def calibrate(port: str = "/dev/ttyAMA0", samples: int = 200, output_path: str = "data/calibration.csv"):
    from src.read_radar import RadarReader

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    reader = RadarReader(port)

    data = []
    for _ in range(samples):
        frame = reader.read_frame()
        if not frame:
            continue
        best = None
        for target in frame:
            if best is None or target["distance_mm"] > best["distance_mm"]:
                best = target
        if best is not None:
            data.append(best["speed_cm_s"])

    reader.close()

    with open(output_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "speed_cm_s"])
        for idx, value in enumerate(data):
            writer.writerow([time.time(), value])

    arr = np.asarray(data, dtype=float)
    processor = SignalProcessor(sampling_rate=10.0)
    bpm = processor.estimate_bpm(arr)
    print(f"Estimated baseline BPM from calibration sample: {bpm:.2f}")
    print(f"Calibration saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calibrate the radar heartbeat sensor")
    parser.add_argument("--port", default="/dev/ttyAMA0")
    parser.add_argument("--samples", type=int, default=200)
    args = parser.parse_args()
    calibrate(port=args.port, samples=args.samples)
