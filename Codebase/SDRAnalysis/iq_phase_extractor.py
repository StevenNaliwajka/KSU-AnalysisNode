import os
from pathlib import Path
import numpy as np
import scipy.signal as signal
import pandas as pd
from datetime import datetime, timedelta
import math

# -------- CONFIG --------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "Data"
OUTPUT_DIR = DATA_DIR / "Train" / "SDR" / "CSV"
TARGET_FREQ_HZ = 491e3  # Example: 100 kHz tone you're tracking
SAMPLE_RATE = 2e6  # Example: 2 MHz HackRF sample rate
SAMPLE_RATIO = 0.01  # % of the samples
MINUTE_BLOCK_SEC = 60
FIXED_FREQ_HZ = 491e6          # Center frequency 491 MHz
RANGE_START_HZ = 489e6         # Range start
RANGE_END_HZ = 492.6e6         # Range end
RANGE_STEPS = 8                # Number of steps in range

# ------------------------

def load_iq_data(iq_file, sample_ratio):
    print(f"  ⏳ Loading IQ data from {iq_file.name}...")
    raw = np.fromfile(iq_file, dtype=np.int8)
    raw_i = raw[0::2]
    raw_q = raw[1::2]
    iq = raw_i.astype(np.float32) + 1j * raw_q.astype(np.float32)

    num_samples = int(len(iq) * sample_ratio)
    print(f"  🔍 Downsampling to {sample_ratio*100:.0f}%: {num_samples} samples...")
    iq = iq[np.random.choice(len(iq), num_samples, replace=False)]
    return iq

def get_avg_phase_over_range(iq_data, fs, start_freq, end_freq, steps):
    freqs = np.linspace(start_freq, end_freq, steps)
    all_phases = []

    for f in freqs:
        phase = get_instantaneous_phase(iq_data, f, fs)
        all_phases.append(phase)

    # Convert to numpy array and average across axis=0 (samples)
    avg_phase = np.mean(all_phases, axis=0)
    return avg_phase


def get_instantaneous_phase(iq_data, target_freq, fs):
    print(f"  🧮 Calculating instantaneous phase at {target_freq/1e3:.1f} kHz...")
    t = np.arange(len(iq_data)) / fs
    osc = np.exp(-1j * 2 * np.pi * target_freq * t)
    mixed = iq_data * osc

    b, a = signal.butter(5, 0.01)
    filtered = signal.lfilter(b, a, mixed)
    phase = np.angle(filtered)
    return phase

def group_by_minute(phases, fs, block_duration_sec):
    print(f"  📊 Grouping phase data into {block_duration_sec}-second blocks...")
    samples_per_block = int(fs * block_duration_sec)
    block_count = math.ceil(len(phases) / samples_per_block)
    avg_phases = []

    for i in range(block_count):
        block = phases[i * samples_per_block: (i + 1) * samples_per_block]
        if len(block) > 0:
            avg_phases.append(np.mean(block))

    print(f"  ✅ Created {len(avg_phases)} averaged phase entries.")
    return avg_phases

def parse_start_time_from_filename(filename):
    try:
        base = Path(filename).stem
        parts = base.split("_")
        dt = datetime.strptime("_".join(parts[:2]), "%Y-%m-%d_%H-%M-%S")
        return dt
    except Exception:
        return None

def process_iq_file(iq_path, output_dir):
    print(f"\n📂 Processing file: {iq_path}")
    try:
        iq = load_iq_data(iq_path, SAMPLE_RATIO)

        # Phase at fixed frequency
        phase_fixed = get_instantaneous_phase(iq, FIXED_FREQ_HZ, SAMPLE_RATE)
        avg_phases_fixed = group_by_minute(phase_fixed, SAMPLE_RATE * SAMPLE_RATIO, MINUTE_BLOCK_SEC)

        # Phase over range
        phase_range = get_avg_phase_over_range(iq, SAMPLE_RATE, RANGE_START_HZ, RANGE_END_HZ, RANGE_STEPS)
        avg_phases_range = group_by_minute(phase_range, SAMPLE_RATE * SAMPLE_RATIO, MINUTE_BLOCK_SEC)

        # Use same time index
        start_time = parse_start_time_from_filename(iq_path.name)
        if start_time is None:
            print("  ⚠️  Failed to parse timestamp from filename. Using current time.")
            start_time = datetime.now()

        times = [start_time + timedelta(minutes=i) for i in range(len(avg_phases_fixed))]

        df = pd.DataFrame({
            "time-date-MIN": times,
            "491MHz": avg_phases_fixed,
            "489-492.6MHz": avg_phases_range
        })

        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / (iq_path.stem + ".csv")
        df.to_csv(out_path, index=False)
        print(f"  💾 Saved CSV to {out_path}")
    except Exception as e:
        print(f"  ❌ Failed to process {iq_path.name}: {e}")


def main():
    print("🔍 Searching for IQ files in:", DATA_DIR)
    found = False
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".iq"):
                found = True
                iq_path = Path(root) / file
                process_iq_file(iq_path, OUTPUT_DIR)

    if not found:
        print("❗ No .iq files found in the Data folder.")

if __name__ == "__main__":
    print("📡 Starting IQ Phase Extraction Script")
    main()
    print("🏁 Done.")
