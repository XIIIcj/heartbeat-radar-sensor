import argparse
import csv
import time
from collections import deque

import numpy as np
from scipy import signal

from src.read_radar import RadarReader
from src.signal_processor import SignalProcessor


class HeartbeatDetector:
    def __init__(self, port: str = "/dev/ttyAMA0", sample_rate: float = 10.0, max_history: int = 200):
        self.reader = RadarReader(port)
        self.processor = SignalProcessor(sampling_rate=sample_rate)
        self.speed_buffer = deque(maxlen=max_history)
        self.timestamps = deque(maxlen=max_history)
        self.last_bpm = None

    def _read_speed(self):
        frame = self.reader.read_frame()
        if not frame:
            return None

        # choose the strongest target by distance or first valid target
        best = None
        for target in frame:
            if best is None:
                best = target
            else:
                if target["distance_mm"] > best["distance_mm"]:
                    best = target
        if best is None:
            return None
        return best["speed_cm_s"]

    def run(self, plot: bool = False):
        if plot:
            import matplotlib.pyplot as plt
            plt.ion()
            fig, ax = plt.subplots()
            line, = ax.plot([], [], lw=2)
            ax.set_ylim(-120, 120)
            ax.set_title("Radar Heartbeat Signal")
            ax.set_xlabel("Samples")
            ax.set_ylabel("Speed (cm/s)")

        while True:
            try:
                speed = self._read_speed()
                if speed is None:
                    continue

                self.speed_buffer.append(float(speed))
                self.timestamps.append(time.time())

                if len(self.speed_buffer) >= 20:
                    samples = np.asarray(self.speed_buffer, dtype=float)
                    bpm_fft = self.processor.estimate_bpm(samples)
                    bpm_peak = self.processor.estimate_bpm_with_peaks(samples)
                    bpm = 0.5 * (bpm_fft + bpm_peak)

                    if bpm > 0:
                        bpm = np.clip(bpm, 30, 200)
                        self.last_bpm = float(bpm)
                        print(f"Estimated BPM: {self.last_bpm:.2f}")

                    if plot:
                        filtered = self.processor.detrend_and_filter(samples)
                        line.set_xdata(np.arange(len(filtered)))
                        line.set_ydata(filtered)
                        ax.relim()
                        ax.autoscale_view()
                        fig.canvas.draw()
                        fig.canvas.flush_events()

            except KeyboardInterrupt:
                print("Stopping heartbeat detector")
                break

        self.reader.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Heartbeat detection with Rd-03D radar")
    parser.add_argument("--port", default="/dev/ttyAMA0")
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    detector = HeartbeatDetector(port=args.port)
    detector.run(plot=args.plot)
