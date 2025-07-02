import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from datetime import datetime

from Codebase.SDRAnalysis.Plot.plot_amplitude_over_time import plot_amplitude_over_time
from Codebase.SDRAnalysis.FileIO.save_plot import save_plot

def plot_amplitude_vs_frequency(iq_data: np.ndarray, sample_rate: float, center_freq: float = 0.0, max_peaks: int = 10):
    """
    2D FFT — Amplitude vs Frequency (dB).
    Detects and prints top N real frequency peaks.
    Allows plotting amplitude over time at selected or all detected frequencies.
    """
    print("🟢 [START] Amplitude vs Frequency")

    N = 2**20
    iq_subset = iq_data[:N]
    fft_vals = np.fft.fftshift(np.fft.fft(iq_subset))
    freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1/sample_rate)) + center_freq
    power_db = 20 * np.log10(np.abs(fft_vals) + 1e-12)

    # --- Detect peaks ---
    noise_floor = np.percentile(power_db, 50)
    prominence_threshold = max(5, np.percentile(power_db, 95) - noise_floor)
    peaks, _ = find_peaks(power_db, prominence=prominence_threshold)

    peak_freqs = freqs[peaks]
    peak_powers = power_db[peaks]

    # Top N peaks
    top_indices = np.argsort(peak_powers)[-max_peaks:][::-1]
    peak_freqs = peak_freqs[top_indices]
    peak_powers = peak_powers[top_indices]

    print(f"📍 Top {max_peaks} Peaks (centered at {center_freq / 1e6:.3f} MHz):")
    labeled_peaks = []
    for idx, (f, p) in enumerate(zip(peak_freqs, peak_powers), 1):
        print(f"  {idx}) {f / 1e6:.3f} MHz @ {p:.1f} dB")
        labeled_peaks.append((idx, f, p))

    # --- Plotting FFT ---
    print("   📊 Plotting FFT...")
    fig = plt.figure(figsize=(10, 4))
    fig.canvas.manager.set_window_title("Amplitude vs Frequency")

    plt.plot(freqs / 1e6, power_db, label="FFT Magnitude")
    plt.plot(peak_freqs / 1e6, peak_powers, 'rx', label="Top Peaks")

    for f, p in zip(peak_freqs, peak_powers):
        plt.annotate(f"{f / 1e6:.2f} MHz", xy=(f / 1e6, p), xytext=(f / 1e6, p + 3),
                     textcoords="data", fontsize=8, ha='center',
                     arrowprops=dict(arrowstyle='->', lw=0.5))

    plt.title("Amplitude vs Frequency")
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    description = f"ampfreq_{center_freq/1e6:.3f}MHz"
    unique_id = f"{max_peaks}peaks"
    filename = f"{timestamp}_{description}_{unique_id}.png"

    save_plot(fig, filename, subfolder="SDR")
    print("✅ [DONE] Amplitude vs Frequency plot saved.")

    # --- Prompt for amplitude-over-time ---
    user_input = input("\n📈 Plot amplitude over time for any of these? (Enter index numbers, or 0 for all): ").strip()
    if user_input:
        selected = [int(x) for x in user_input.split() if x.isdigit()]
        if 0 in selected:
            selected = [idx for idx, _, _ in labeled_peaks]  # All
        for sel in selected:
            match = next((f for i, f, _ in labeled_peaks if i == sel), None)
            if match:
                print(f"🕒 Plotting amplitude over time for {match / 1e6:.3f} MHz...")
                plot_amplitude_over_time(iq_data, sample_rate, center_freq, match)
