import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, correlate


def extract_pulse(iq_data: np.ndarray, start_index: int, duration_ms: float, sample_rate: float) -> np.ndarray:
    """
    Extracts a snippet of the IQ data representing a pulse of given duration starting from a given index.
    """
    length = int(duration_ms * sample_rate / 1000.0)
    return iq_data[start_index:start_index + length]