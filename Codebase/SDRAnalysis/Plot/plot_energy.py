import matplotlib
matplotlib.use('TkAgg')  # Ensure GUI backend is used

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from Codebase.SDRAnalysis.FileIO.save_plot import save_plot

def plot_energy(energy: np.ndarray, sample_count: int = 1_000_000):
    """
    Plots signal energy for a given number of samples.
    Saves the plot to file instead of displaying.
    """
    print("🟢 [START] Signal Energy Plot")

    fig = plt.figure(figsize=(10, 4))
    fig.canvas.manager.set_window_title("Signal Energy")
    plt.plot(energy[:sample_count], linewidth=1.0)
    plt.title("Pulse Detection via Signal Energy")
    plt.xlabel("Sample Index")
    plt.ylabel("Energy")
    plt.grid(True)
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    description = "signal_energy"
    unique_id = f"samples{sample_count}"
    filename = f"{timestamp}_{description}_{unique_id}.png"

    save_plot(fig, filename, subfolder="SDR")
    print("✅ [DONE] Signal Energy plot saved.")
