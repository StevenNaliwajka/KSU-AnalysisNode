import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, correlate

def compute_signal_energy(iq_data: np.ndarray, sample_rate: float, window_ms: float = 1.0) -> np.ndarray:
    """
    Computes short-term signal energy over the specified window (in milliseconds).
    """
    power = np.abs(iq_data) ** 2
    window = int(window_ms * sample_rate / 1000.0)
    energy = np.convolve(power, np.ones(window), mode='valid')
    return energy