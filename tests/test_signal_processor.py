# tests for radar heartbeat detector

import numpy as np

from src.signal_processor import SignalProcessor


def test_signal_estimation():
    fs = 10.0
    t = np.arange(0, 30, 1.0 / fs)
    signal_data = 25 * np.sin(2 * np.pi * 1.2 * t) + 5 * np.sin(2 * np.pi * 0.3 * t)

    processor = SignalProcessor(sampling_rate=fs)
    bpm = processor.estimate_bpm(signal_data)
    assert 60 <= bpm <= 120


def test_peak_based_estimation():
    fs = 10.0
    t = np.arange(0, 30, 1.0 / fs)
    signal_data = 30 * np.sin(2 * np.pi * 1.4 * t)

    processor = SignalProcessor(sampling_rate=fs)
    bpm = processor.estimate_bpm_with_peaks(signal_data)
    assert 70 <= bpm <= 110
