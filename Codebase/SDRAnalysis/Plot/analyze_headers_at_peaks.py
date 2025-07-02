import numpy as np
from scipy.signal import find_peaks

from Codebase.SDRAnalysis.Analysis.compute_signal_energy import compute_signal_energy
from Codebase.SDRAnalysis.Analysis.extract_pulse import extract_pulse
from Codebase.SDRAnalysis.Analysis.correlate_with_pulse import correlate_with_pulse
from Codebase.SDRAnalysis.Plot.plot_correlation import plot_correlation

def analyze_headers_at_peaks(
    iq_data: np.ndarray,
    sample_rate: float,
    center_freq: float,
    bandwidth_hz: float = 200_000,
    header_duration_ms: float = 2.0
):
    print("\n🔎 Detecting peaks in frequency spectrum...")

    # Compute FFT and amplitude spectrum
    fft_data = np.fft.fftshift(np.fft.fft(iq_data))
    freqs = np.fft.fftshift(np.fft.fftfreq(len(iq_data), d=1 / sample_rate))
    amplitude = np.abs(fft_data)

    # Find peaks above a threshold
    peak_indices, _ = find_peaks(amplitude, height=np.max(amplitude) * 0.3)
    peak_freqs = freqs[peak_indices] + center_freq

    if not len(peak_freqs):
        print("⚠️  No peaks found. Skipping header analysis.")
        return

    print(f"\n🔬 Starting header analysis for {len(peak_freqs)} peaks...")
    for i, freq in enumerate(peak_freqs):
        print(f"\n🔍 [HEADER DETECTION] Peak {i+1}/{len(peak_freqs)}: {freq / 1e6:.3f} MHz")

        # Shift to baseband
        delta_f = freq - center_freq
        print(f"   ↪ Shifting by Δf = {delta_f:.1f} Hz")
        n = np.arange(len(iq_data))
        shifted = iq_data * np.exp(-1j * 2 * np.pi * delta_f * n / sample_rate)

        # Filter in frequency domain
        print("   ↪ Filtering in frequency domain...")
        fft_len = len(shifted)
        spectrum = np.fft.fftshift(np.fft.fft(shifted))
        freqs_local = np.fft.fftshift(np.fft.fftfreq(fft_len, d=1/sample_rate))
        mask = np.abs(freqs_local) < (bandwidth_hz / 2)
        spectrum_filtered = np.zeros_like(spectrum)
        spectrum_filtered[mask] = spectrum[mask]
        filtered = np.fft.ifft(np.fft.ifftshift(spectrum_filtered))

        # Energy detection
        print("   ↪ Computing energy signal...")
        energy = compute_signal_energy(filtered, sample_rate=sample_rate, window_ms=1.0)
        peak_idx = np.argmax(energy)
        print(f"   ↪ Header candidate peak at index: {peak_idx}")

        # Extract pulse (potential header)
        print("   ↪ Extracting header pulse...")
        header = extract_pulse(filtered, start_index=peak_idx, duration_ms=header_duration_ms, sample_rate=sample_rate)

        # Correlate against full signal
        print("   ↪ Running correlation against entire signal...")
        correlation = correlate_with_pulse(filtered, header)

        # Save correlation plot
        print("   ↪ Saving correlation plot...")
        plot_correlation(correlation)

    print("\n✅ Header analysis complete.")
