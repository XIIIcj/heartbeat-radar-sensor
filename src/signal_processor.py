import numpy as np
from scipy import signal


class SignalProcessor:
    def __init__(self, sampling_rate: float = 10.0, low_hz: float = 0.8, high_hz: float = 3.0):
        self.sampling_rate = sampling_rate
        self.low_hz = low_hz
        self.high_hz = high_hz

    def detrend_and_filter(self, samples: np.ndarray) -> np.ndarray:
        if len(samples) < 5:
            return samples
        detrended = signal.detrend(samples, type="constant")
        b, a = signal.butter(4, [self.low_hz / (self.sampling_rate / 2.0), self.high_hz / (self.sampling_rate / 2.0)], btype="bandpass")
        filtered = signal.filtfilt(b, a, detrended)
        return filtered

    def estimate_bpm(self, samples: np.ndarray) -> float:
        if len(samples) < 20:
            return 0.0

        filtered = self.detrend_and_filter(samples)
        freqs = np.fft.rfftfreq(len(filtered), d=1.0 / self.sampling_rate)
        spectrum = np.abs(np.fft.rfft(filtered))

        # ignore dc and only consider plausible cardiac frequencies
        mask = (freqs >= self.low_hz) & (freqs <= self.high_hz)
        if not np.any(mask):
            return 0.0

        valid_freqs = freqs[mask]
        valid_spectrum = spectrum[mask]
        dominant_idx = np.argmax(valid_spectrum)
        dominant_freq = valid_freqs[dominant_idx]
        bpm = dominant_freq * 60.0
        return float(bpm)

    def estimate_bpm_with_peaks(self, samples: np.ndarray) -> float:
        filtered = self.detrend_and_filter(samples)
        peaks, _ = signal.find_peaks(filtered, distance=max(1, int(self.sampling_rate * 0.35)))
        if len(peaks) < 2:
            return self.estimate_bpm(samples)

        # Estimate inter-beat interval in seconds
        peak_times = np.diff(peaks) / self.sampling_rate
        if len(peak_times) == 0:
            return self.estimate_bpm(samples)

        avg_interval = np.median(peak_times)
        if avg_interval <= 0:
            return self.estimate_bpm(samples)

        bpm = 60.0 / avg_interval
        return float(bpm)
