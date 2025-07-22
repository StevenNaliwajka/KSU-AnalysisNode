import os
import matplotlib.pyplot as plt

def save_plot(fig, filename: str, subfolder: str = "SDR", dpi: int = 300):
    """
    Saves a matplotlib figure to Output/SDR/{filename}.png

    Args:
        fig: matplotlib figure object
        filename: Descriptive filename (no extension)
        subfolder: Subdirectory inside Output/ (default: "SDR")
        dpi: Image resolution in dots per inch (default: 300)
    """
    base_dir = os.path.join("Output", subfolder)
    os.makedirs(base_dir, exist_ok=True)

    full_path = os.path.join(base_dir, f"{filename}.png")
    fig.savefig(full_path, dpi=dpi, bbox_inches="tight")
    print(f"💾 Saved plot to: {full_path}")
