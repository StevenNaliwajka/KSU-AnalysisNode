import matplotlib.pyplot as plt
import numpy as np

from Codebase.SDRAnalysis.FileIO.save_plot import save_plot

def plot_correlation(correlation: np.ndarray, peak_index: int = None, freq_label: str = None):
    """
    Plots the correlation result and optionally zooms in around the detected peak.

    Args:
        correlation: Correlation result array.
        peak_index: Optional index of peak to zoom in on.
        freq_label: Optional label (e.g. frequency in MHz) to add to filename.
    """
    # Plot full correlation
    fig1 = plt.figure(figsize=(10, 4))
    plt.plot(np.abs(correlation))
    plt.title("Full Correlation Result")
    plt.xlabel("Sample Index")
    plt.ylabel("Correlation Magnitude")
    plt.grid(True)
    plt.tight_layout()

    label = f"_peak_{freq_label}" if freq_label else ""
    save_plot(fig1, f"correlation_full{label}")

    # Plot zoomed-in correlation around peak
    if peak_index is None:
        peak_index = np.argmax(np.abs(correlation))

    window = 200  # samples left/right of peak
    start = max(peak_index - window, 0)
    end = min(peak_index + window, len(correlation))

    fig2 = plt.figure(figsize=(10, 4))
    plt.plot(np.abs(correlation[start:end]))
    plt.title(f"Zoomed Correlation Around Peak @ Index {peak_index}")
    plt.xlabel("Sample Index")
    plt.ylabel("Correlation Magnitude")
    plt.grid(True)
    plt.tight_layout()

    save_plot(fig2, f"correlation_zoomed{label}")
