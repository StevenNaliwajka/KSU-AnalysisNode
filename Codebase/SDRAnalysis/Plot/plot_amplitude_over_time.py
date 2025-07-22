import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from Codebase.SDRAnalysis.FileIO.save_plot import save_plot

def plot_amplitude_over_time(
    iq_data: np.ndarray,
    sample_rate: float,
    center_freq_hz: float,
    target_freq_hz: float,
    bandwidth_hz: float = 200_000,
    time_bin_ms: float = 1.0
):
    """
    Plot average amplitude over time in a narrow frequency band.
    """
    print("🟢 [START] Amplitude vs Time")
    print(f"   • Center Frequency  : {center_freq_hz/1e6:.3f} MHz")
    print(f"   • Target Frequency  : {target_freq_hz/1e6:.3f} MHz")
    print(f"   • Bandwidth         : ±{bandwidth_hz/2/1e3:.0f} kHz")
    print(f"   • Time Bin Duration : {time_bin_ms:.1f} ms")

    # Step 1: Shift frequency
    delta_f = target_freq_hz - center_freq_hz
    print(f"   ↪ Frequency shift applied: {delta_f/1e3:.1f} kHz")
    n = np.arange(len(iq_data))
    iq_shifted = iq_data * np.exp(-1j * 2 * np.pi * delta_f * n / sample_rate)

    # Step 2: Low-pass filter via FFT (apply frequency mask)
    print("   ↪ Applying frequency mask and filtering...")
    fft_len = len(iq_shifted)
    spectrum = np.fft.fftshift(np.fft.fft(iq_shifted))
    freqs = np.fft.fftshift(np.fft.fftfreq(fft_len, d=1/sample_rate))

    mask = np.abs(freqs) < (bandwidth_hz / 2)
    spectrum_filtered = np.zeros_like(spectrum)
    spectrum_filtered[mask] = spectrum[mask]

    iq_filtered = np.fft.ifft(np.fft.ifftshift(spectrum_filtered))

    # Step 3: Compute amplitude per time bin
    bin_size = int(sample_rate * time_bin_ms / 1000)
    num_bins = len(iq_filtered) // bin_size
    print(f"   ↪ Binning {len(iq_filtered)} samples into {num_bins} bins of {bin_size} each...")
    iq_trimmed = iq_filtered[:num_bins * bin_size]
    iq_binned = iq_trimmed.reshape((num_bins, bin_size))
    amplitudes = np.abs(iq_binned).mean(axis=1)

    times = np.arange(num_bins) * (time_bin_ms / 1000)

    # Step 4: Plot
    print("   📊 Plotting...")
    fig = plt.figure(figsize=(10, 4))
    fig.canvas.manager.set_window_title("Amplitude over Time")

    plt.plot(times, amplitudes)
    plt.title(f"Amplitude Over Time @ {target_freq_hz/1e6:.3f} MHz")
    plt.xlabel("Time (s)")
    plt.ylabel("Average Amplitude")
    plt.grid(True)
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    description = f"amptime_{target_freq_hz/1e6:.3f}MHz"
    unique_id = f"{int(time_bin_ms)}ms"
    filename = f"{timestamp}_{description}_{unique_id}.png"

    save_plot(fig, filename, subfolder="SDR")
    print("✅ [DONE] Plot saved.")