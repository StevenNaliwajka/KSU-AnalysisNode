import matplotlib.pyplot as plt
import numpy as np

from Codebase.SDRAnalysis.Analysis.compute_signal_energy import compute_signal_energy
from Codebase.SDRAnalysis.Analysis.extract_pulse import extract_pulse
from Codebase.SDRAnalysis.Analysis.correlate_with_pulse import correlate_with_pulse
from Codebase.SDRAnalysis.Plot.analyze_headers_at_peaks import analyze_headers_at_peaks

from Codebase.SDRAnalysis.FileIO.load_hackrf_iq import load_hackrf_iq

from Codebase.SDRAnalysis.Plot.plot_spectrogram import plot_spectrogram
from Codebase.SDRAnalysis.Plot.plot_energy import plot_energy
from Codebase.SDRAnalysis.Plot.plot_pulse import plot_pulse
from Codebase.SDRAnalysis.Plot.plot_correlation import plot_correlation
from Codebase.SDRAnalysis.Plot.plot_amplitude_vs_frequency import plot_amplitude_vs_frequency
from Codebase.SDRAnalysis.Plot.plot_3d_spectrogram import plot_3d_spectrogram
from Codebase.SDRAnalysis.Plot.plot_amplitude_over_time import plot_amplitude_over_time


def main():
    fs = 20e6  # Sample rate in Hz
    center_freq = 491_000_000  # Hz

    print("\U0001f4e1 [START] Loading IQ data...")
    iq_data = load_hackrf_iq()
    print("✅ IQ data loaded.\n")

    energy = None
    pulse = None
    correlation = None
    fft_peaks = []

    plot_dispatch = {
        "1": {
            "name": "Spectrogram (2D)",
            "func": lambda: plot_spectrogram(iq_data[:int(fs * 1.0)], fs)
        },
        "2": {
            "name": "Signal Energy",
            "func": lambda: plot_energy(_get_energy())
        },
        "3": {
            "name": "Extracted Pulse",
            "func": lambda: plot_pulse(_get_pulse())
        },
        "4": {
            "name": "Correlation with Pulse",
            "func": lambda: plot_correlation(_get_correlation())
        },
        "5": {
            "name": "Amplitude vs Frequency (FFT)",
            "func": lambda: _run_fft()
        },
        "6": {
            "name": "3D Spectrogram",
            "func": lambda: plot_3d_spectrogram(iq_data, fs, max_seconds=0.5)
        },
        "7": {
            "name": "Amplitude Over Time @ Frequency",
            "func": lambda: plot_amplitude_over_time(
                iq_data,
                sample_rate=fs,
                center_freq_hz=center_freq,
                target_freq_hz=float(input("↪ Enter target frequency in Hz (e.g. 486000000): ").strip())
            )
        },
        "8": {
            "name": "Analyze Headers at Detected Peaks",
            "func": lambda:         analyze_headers_at_peaks(
                iq_data=iq_data,
                sample_rate=fs,
                center_freq=center_freq,
                bandwidth_hz=200_000,
                header_duration_ms=2.0
            )
        }
    }

    def _analyze_headers_with_fft():
        nonlocal fft_peaks
        if not fft_peaks:
            print("⚠️  No FFT peaks found. Automatically running FFT first...")
            fft_peaks = plot_amplitude_vs_frequency(iq_data, fs, center_freq=center_freq)
        if fft_peaks:
            analyze_headers_at_peaks(
                iq_data,
                sample_rate=fs,
                center_freq=center_freq,
                peak_freqs=fft_peaks,
                bandwidth_hz=200_000,
                header_duration_ms=2.0
            )
        else:
            print("🚫 Still no peaks detected. Skipping header analysis.")

    def _get_energy():
        nonlocal energy
        if energy is None:
            print("↪ Computing signal energy...")
            energy = compute_signal_energy(iq_data, sample_rate=fs, window_ms=1.0)
        return energy

    def _get_pulse():
        nonlocal pulse
        if pulse is None:
            e = _get_energy()
            peak_idx = e.argmax()
            print(f"↪ Extracting pulse from peak index {peak_idx}...")
            pulse = extract_pulse(iq_data, start_index=peak_idx, duration_ms=2.0, sample_rate=fs)
        return pulse

    def _get_correlation():
        nonlocal correlation
        if correlation is None:
            p = _get_pulse()
            print("↪ Correlating with extracted pulse...")
            correlation = correlate_with_pulse(iq_data, p)
        return correlation

    def _run_fft():
        nonlocal fft_peaks
        print("↪ Running FFT to find peaks...")
        fft_peaks = plot_amplitude_vs_frequency(iq_data, fs, center_freq=center_freq)

    print("🔢 Available Plots:")
    for k in sorted(plot_dispatch):
        print(f"  {k}) {plot_dispatch[k]['name']}")

    try:
        user_input = input("\nEnter plot numbers (e.g., 1 2 5) or 'all': ").strip().lower()
        selected = list(plot_dispatch.keys()) if user_input == "all" else user_input.split()
    except KeyboardInterrupt:
        print("\n🛑 Cancelled by user during input.")
        return

    try:
        for key in selected:
            if key in plot_dispatch:
                name = plot_dispatch[key]["name"]
                print(f"📊 Generating: {name}")
                plot_dispatch[key]["func"]()
            else:
                print(f"⚠️  Invalid option: {key}")
    except KeyboardInterrupt:
        print("\n🛑 Cancelled during plot generation.")
        return

    print("\n✅ Plot generation complete. Check the 'Output/SDR' folder for saved images.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Program interrupted.")