# tests for heartbeat detector

import numpy as np

from src.signal_processor import SignalProcessor


def test_frequency_mapping():
    fs = 10.0
    t = np.arange(0, 20, 1.0 / fs)
    signal_data = 20 * np.sin(2 * np.pi * 1.0 * t)

    processor = SignalProcessor(sampling_rate=fs)
    bpm = processor.estimate_bpm(signal_data)

    assert abs(bpm - 60.0) < 10.0
