import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, correlate


def correlate_with_pulse(iq_data: np.ndarray, pulse: np.ndarray) -> np.ndarray:
    """
    Performs magnitude-based correlation of the IQ data with the extracted pulse.
    """
    correlation = correlate(np.abs(iq_data), np.abs(pulse), mode='valid')
    return correlation