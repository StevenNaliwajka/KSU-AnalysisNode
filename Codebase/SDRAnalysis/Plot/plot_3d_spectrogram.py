import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from datetime import datetime
from Codebase.SDRAnalysis.FileIO.save_plot import save_plot

def plot_3d_spectrogram(iq_data: np.ndarray, sample_rate: float, max_seconds: float = 0.5):
    """
    Plot 2: 3D Amplitude vs Time vs Frequency surface
    """
    print("[3D Plot] Generating spectrogram data...")
    iq_data = iq_data[:int(sample_rate * max_seconds)]

    f, t, Sxx = spectrogram(iq_data, fs=sample_rate, nperseg=1024, noverlap=512)
    Z = 10 * np.log10(Sxx + 1e-12)

    print("[3D Plot] Plotting 3D surface...")
    T, F = np.meshgrid(t, f / 1e6)  # frequency in MHz

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(T, F, Z, cmap='viridis')

    ax.set_title("3D Spectrogram: Amplitude vs Time vs Frequency")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (MHz)")
    ax.set_zlabel("Power (dB)")
    fig.colorbar(surf, shrink=0.5, aspect=10)
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    description = f"spec3d_{max_seconds:.1f}s"
    unique_id = "surface"
    filename = f"{timestamp}_{description}_{unique_id}.png"

    save_plot(fig, filename, subfolder="SDR")