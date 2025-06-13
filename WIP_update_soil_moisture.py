import os
import pandas as pd

# Constants
WET = 110
DRY = 688
RAWDATA_DIR = "RawData"

def calculate_percent_wet(value):
    wet = 110
    dry = 688
    percent = 100 * (1 - (value - wet) / (dry - wet))
    return round(max(0, min(100, percent)), 2)


def process_csv(file_path):
    # Read skipping first two rows manually
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Get header and data rows
    header1, header2 = lines[:2]
    data = pd.read_csv(file_path, skiprows=2)

    if "Soil Moisture Value" not in data.columns or "Soil Moisture (%)" not in data.columns:
        print(f"[SKIP] Missing required columns in {file_path}")
        return

    data["Soil Moisture (%)"] = data["Soil Moisture Value"].apply(calculate_percent_wet)

    with open(file_path, 'w') as f:
        f.write(header1)
        f.write(header2)
        data.to_csv(f, index=False)

    print(f"[OK] Updated {file_path}")

def main():
    for root, _, files in os.walk(RAWDATA_DIR):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                try:
                    process_csv(file_path)
                except Exception as e:
                    print(f"[ERROR] Failed processing {file_path}: {e}")

if __name__ == "__main__":
    main()
