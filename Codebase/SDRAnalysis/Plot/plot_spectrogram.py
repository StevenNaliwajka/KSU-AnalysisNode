import matplotlib
matplotlib.use('TkAgg')  # GUI backend

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from datetime import datetime

from Codebase.SDRAnalysis.FileIO.save_plot import save_plot

def plot_spectrogram(iq_data: np.ndarray, sample_rate: float):
    """
    Plots the spectrogram of the IQ data to identify frequency activity over time.
    Saves the plot to file instead of displaying.
    """
    print("🟢 [START] Spectrogram Plot")

    f, t, Sxx = spectrogram(iq_data, fs=sample_rate, nperseg=2048, noverlap=1024)
    Z = 10 * np.log10(Sxx + 1e-12)  # avoid log(0)
    vmin = np.percentile(Z, 5)
    vmax = np.percentile(Z, 99)

    fig = plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f / 1e6, Z, shading='auto', vmin=vmin, vmax=vmax)
    plt.title("Spectrogram")
    plt.ylabel("Frequency (MHz)")
    plt.xlabel("Time (s)")
    plt.colorbar(label="Power (dB)")
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    description = "spectrogram"
    unique_id = f"{int(sample_rate/1e6)}Msps"
    filename = f"{timestamp}_{description}_{unique_id}.png"

    save_plot(fig, filename, subfolder="SDR")
    print("✅ [DONE] Spectrogram plot saved.")