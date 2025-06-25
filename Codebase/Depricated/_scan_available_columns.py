import os
from pathlib import Path

# Constants
ROOT_DATA_PATH = Path(__file__).resolve().parents[2] / "Data"
BLACKLIST_PATH = Path(__file__).resolve().parents[2] / "Config" / "dropdown_blacklist.txt"
SUBFOLDERS = ["Predict", "Train"]

# Determines where the header is for each data type
HEADER_LINE_MAP = {
    "Atmospheric": 0,
    "SDR": 2,
    "Soil": 2,
    "TVWS": 2
}

def scan_first_valid_csv(folder: Path, skip_rows: int):
    """Scan the first valid CSV file in the folder and return cleaned header columns."""
    for root, _, files in os.walk(folder):
        for file in sorted(files):  # sorted for reproducibility
            if file.lower().endswith(".csv"):
                path = Path(root) / file
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        if len(lines) > skip_rows:
                            return [col.strip().lower() for col in lines[skip_rows].split(",")]
                except Exception as e:
                    print(f"[ERROR] Couldn't read {path}: {e}")
    return []

def scan_available_columns():
    """Scan each data type folder and extract available column names, excluding blacklisted ones."""
    seen_types = set()
    available_columns = {}
    blacklist = load_blacklist()

    for subdir in SUBFOLDERS:
        base_path = ROOT_DATA_PATH / subdir

        for data_type, skip_rows in HEADER_LINE_MAP.items():
            if data_type in seen_types:
                continue  # Already scanned

            data_folder = base_path / data_type
            if not data_folder.exists():
                continue

            columns = scan_first_valid_csv(data_folder, skip_rows)
            if columns:
                filtered = [col for col in columns if col not in blacklist]
                available_columns[data_type] = filtered
                seen_types.add(data_type)

    return available_columns

if __name__ == "__main__":
    from pprint import pprint
    pprint(scan_available_columns())
