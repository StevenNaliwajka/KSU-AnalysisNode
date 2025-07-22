import matplotlib
matplotlib.use('TkAgg')  # Ensure GUI backend is used

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from Codebase.SDRAnalysis.FileIO.save_plot import save_plot

def plot_pulse(pulse: np.ndarray):
    """
    Plots the magnitude of an extracted pulse.
    Saves the plot to file instead of displaying.
    """
    print("🟢 [START] Extracted Pulse Plot")

    fig = plt.figure(figsize=(8, 4))
    fig.canvas.manager.set_window_title("Extracted Pulse")
    plt.plot(np.abs(pulse), linewidth=1.0)
    plt.title("Extracted Pulse (Magnitude)")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    description = "extracted_pulse"
    unique_id = f"samples{len(pulse)}"
    filename = f"{timestamp}_{description}_{unique_id}.png"

    save_plot(fig, filename, subfolder="SDR")
    print("✅ [DONE] Extracted Pulse plot saved.")
