from Codebase.DataManager.data_loader import DataLoader
from pathlib import Path
from collections import defaultdict

# --- Load blacklist ---
def load_blacklist():
    blacklist_path = Path(__file__).resolve().parent / "dropdown_blacklist.txt"
    if not blacklist_path.exists():
        print(f"[WARN] No blacklist file found at: {blacklist_path}")
        return set()
    with open(blacklist_path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

# --- Initialize ---
loader = DataLoader()
csv_files = loader.get_all_csv_files_recursively()
blacklist = load_blacklist()

# --- Map from file name to data type and header line index ---
type_map = {
    "soil": ("Soil", 2),
    "tvws": ("TVWS", 2),
    "sdr": ("SDR", 2),
    "ambient": ("Atmospheric", 0),
}

available_columns_by_type = defaultdict(set)
scanned_types = set()

# --- Scan one file per type for columns ---
for file_path in csv_files:
    filename = str(file_path).lower()

    for key, (data_type, header_line_index) in type_map.items():
        if key in filename and data_type not in scanned_types:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                if len(lines) > header_line_index:
                    header_line = lines[header_line_index].strip()
                    columns = [
                        c.strip().strip('"').strip("'").lower()
                        for c in header_line.split(",")
                    ]
                    for col in columns:
                        if col not in blacklist:
                            available_columns_by_type[data_type].add(col)
                    scanned_types.add(data_type)
                    print(f"[INFO] Scanned {data_type} headers from: {file_path.name}")
            except Exception as e:
                print(f"[ERROR] Reading {file_path}: {e}")
            break  # Done checking keys once matched

# --- Preload CSVs into memory (optional but useful for dashboard) ---
for file_path in csv_files:
    filename = str(file_path).lower()
    for key, (data_type, skip_rows) in type_map.items():
        if key in filename:
            try:
                df = loader.read_csv(file_path, header_line=skip_rows)
                if df is not None:
                    loader.add_to_data(data_type, str(file_path), df)
            except Exception as e:
                print(f"[ERROR] Failed to load {file_path.name}: {e}")
            break

# --- Finalize exposed metadata ---
available_columns_by_type = {k: sorted(v) for k, v in available_columns_by_type.items()}
all_available_columns = sorted({col for cols in available_columns_by_type.values() for col in cols})

# --- Expose globally ---
__all__ = ["available_columns_by_type", "all_available_columns", "loader"]
