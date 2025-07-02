import os
import argparse
import numpy as np

def split_iq_file(filename, sample_rate, output_dir=None):
    # Constants
    samples_per_sec = int(sample_rate)
    bytes_per_sample = 2  # 1 byte I + 1 byte Q

    # Setup output path
    if output_dir is None:
        output_dir = os.path.dirname(filename)
    os.makedirs(output_dir, exist_ok=True)

    # Read file
    with open(filename, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.int8)

    total_samples = len(data) // bytes_per_sample
    total_seconds = total_samples // samples_per_sec
    base_name = os.path.splitext(os.path.basename(filename))[0]

    print(f"Total samples: {total_samples}")
    print(f"Splitting into {total_seconds} full seconds...")

    for i in range(total_seconds):
        start = i * samples_per_sec * bytes_per_sample
        end = (i + 1) * samples_per_sec * bytes_per_sample
        chunk = data[start:end]
        out_path = os.path.join(output_dir, f"{base_name}_{i+1}.iq")
        chunk.tofile(out_path)
        print(f"Saved: {out_path}")

    # Handle leftover samples
    leftover_start = total_seconds * samples_per_sec * bytes_per_sample
    leftover = data[leftover_start:]
    if leftover.size > 0:
        out_path = os.path.join(output_dir, f"{base_name}_part{total_seconds+1}.iq")
        leftover.tofile(out_path)
        print(f"Saved leftover: {out_path} ({leftover.size // 2} samples)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split .iq file into 1-second chunks.")
    parser.add_argument("filename", help="Input .iq file path")
    parser.add_argument("--rate", type=float, default=20e6, help="Sample rate (Hz), default 20 MHz")
    parser.add_argument("--out", default=None, help="Optional output directory")
    args = parser.parse_args()

    split_iq_file(args.filename, args.rate, args.out)

