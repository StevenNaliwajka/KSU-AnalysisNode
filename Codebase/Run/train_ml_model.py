from datetime import datetime

import pandas as pd
from pathlib import Path
import json
from collections import defaultdict
from sklearn.utils import shuffle
from Codebase.CorrelationModeling.PolyRegression.poly_train import train_model
from Codebase.CorrelationModeling.model_loader import save_model
from Codebase.DataManager.data_loader import DataLoader
from Codebase.Pathing.get_project_root import get_project_root
import logging
import traceback

logging.basicConfig(filename="train_debug.log", level=logging.DEBUG)

print("=== [Train a New ML Model] ===\n")

loader = DataLoader()
project_root = get_project_root()
train_dir = project_root / "Data" / "Train"
config_path = project_root / "Codebase" / "CorrelationModeling" / "merge_config.json"

# Load config
if not config_path.exists():
    print(f"[✖] Missing config file: {config_path}")
    exit(1)

with open(config_path) as f:
    config = json.load(f)
merge_tolerance = int(config.get("merge_tolerance_seconds", 60))

# === Scan first CSV in each folder ===
print("[Discovered Unique Header Types Across First Files of Folders]:")

header_sources = {}
col_id_map = {}
col_id = 1

for subdir in train_dir.iterdir():
    if subdir.is_dir():
        print(f"\n[INFO] Starting header discovery in: {subdir.name}")
        first_csv = next(subdir.glob("*.csv"), None)
        if not first_csv:
            continue
        try:
            if "ambient-weather" in first_csv.name.lower():
                df = loader.read_csv(first_csv, skip_rows=1)
            else:
                df = loader.read_csv(first_csv, skip_rows=2)

            print(f"[DEBUG] Loaded file: {first_csv.name} — shape: {df.shape}")

            if "Date" in df.columns and "Time" in df.columns:
                df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors='coerce', utc=True)
            elif "Date" in df.columns:
                df["datetime"] = pd.to_datetime(df["Date"], errors='coerce', utc=True)
            else:
                df["datetime"] = pd.to_datetime(df.iloc[:, 0], errors='coerce', utc=True)

            print(f"[DEBUG] Parsed datetime column — non-null count: {df['datetime'].notnull().sum()}")

            for col in df.columns:
                if col.lower().startswith("date") or col.lower().startswith("time") or col == "datetime":
                    continue
                if col not in header_sources:
                    header_sources[col] = first_csv
                    col_id_map[str(col_id)] = col
                    print(f"[{col_id}] {col} (from {first_csv.name})")
                    col_id += 1
        except Exception as e:
            print(f"[ERROR] {first_csv.name}: {e}")
            logging.exception(f"Failed loading {first_csv.name}")

if len(col_id_map) < 2:
    print("[✖] Not enough unique columns to continue.")
    exit(1)

# === User Selection ===
print(f"\n[INFO] Awaiting user input for column selection...")
input_indices = input("\nSelect input columns (e.g., 13): ").split(",")
output_index = input("Select output column (e.g., 1): ").strip()

try:
    input_headers = [col_id_map[i.strip()] for i in input_indices if i.strip() in col_id_map]
    output_header = col_id_map[output_index]
except KeyError:
    print("[✖] Invalid input/output selection.")
    exit(1)

selected_headers = input_headers + [output_header]

# === Load only one matching file per selected column ===
used_headers = set()
files_to_merge = []

for f in sorted(train_dir.rglob("*.csv")):
    try:
        if "ambient-weather" in f.name.lower():
            df = loader.read_csv(f, skip_rows=1)
        else:
            df = loader.read_csv(f, skip_rows=2)

        if "Date" in df.columns and "Time" in df.columns:
            df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors='coerce', utc=True)
        elif "Date" in df.columns:
            df["datetime"] = pd.to_datetime(df["Date"], errors='coerce', utc=True)
        else:
            df["datetime"] = pd.to_datetime(df.iloc[:, 0], errors='coerce', utc=True)

        df = df.dropna(subset=["datetime"])

        # Only include this file if it has one or more headers we still need
        available = [col for col in selected_headers if col in df.columns and col not in used_headers]
        if available:
            print(f"[DEBUG] Using file: {f.name} — columns: {available}")
            used_headers.update(available)
            files_to_merge.append((f.name, df[["datetime"] + available]))

        if used_headers == set(selected_headers):
            break  # Done loading what we need

    except Exception as e:
        print(f"[ERROR loading {f.name}]: {e}")
        logging.exception(f"Failed during data load: {f.name}")

# === Merge files safely ===
if len(files_to_merge) < 2:
    print("[✖] Not enough matching data to continue.")
    exit(1)

print("[INFO] Starting merge process...")
base_df = files_to_merge[0][1].copy()
base_df["datetime_rounded"] = base_df["datetime"].dt.floor(f"{merge_tolerance}s")
base_df = base_df.drop_duplicates(subset="datetime_rounded", keep="first")

for fname, df in files_to_merge[1:]:
    df = df.copy()
    df["datetime_rounded"] = df["datetime"].dt.floor(f"{merge_tolerance}s")
    df = df.drop_duplicates(subset="datetime_rounded", keep="first")
    print(f"[DEBUG] Merging file: {fname} — columns: {df.columns.tolist()}")
    base_df = pd.merge(base_df, df, on="datetime_rounded", suffixes=("", f"_{fname}"))

if base_df.empty:
    print("[✖] No overlap found after merging.")
    exit(1)

# === Build final train DataFrame ===
train_df = base_df[["datetime_rounded"] + input_headers + [output_header]].dropna()
train_df = train_df.rename(columns={"datetime_rounded": "time"})
train_df = train_df[["time"] + input_headers + [output_header]]

if train_df.empty:
    print("[✖] No valid training rows after dropping NaNs.")
    exit(1)

print(f"[INFO] Final training data shape: {train_df.shape}")
print(f"[INFO] Training model with inputs: {input_headers} → output: {output_header}")

if len(train_df) < 2:
    print("[✖] Not enough data to split for training. Try different columns or more data.")
    exit(1)

train_df = shuffle(train_df)

degree_input = input("Enter polynomial degree [default = 2]: ").strip()
degree = int(degree_input) if degree_input else 2

print("\n[INFO] Training model...")
model, score = train_model(train_df, input_headers, output_header, degree)
print(f"[INFO] Model R² Score: {score:.3f}")

# Generate default save path
timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
default_model_name = f"model_{timestamp_str}.joblib"
model_dir = project_root / "Codebase" / "CorrelationModeling" / "MLBinary"
model_dir.mkdir(parents=True, exist_ok=True)
model_path = model_dir / default_model_name

# Prompt user to override
user_input = input(f"Save model as [default: {model_path}]: ").strip()
if user_input:
    model_path = Path(user_input)

# Save model binary
save_model(model, str(model_path))

# Save metadata about model
metadata = {
    "inputs": input_headers,
    "output": output_header,
    "degree": degree
}
with open(model_path.with_suffix(".json"), "w") as meta_file:
    json.dump(metadata, meta_file, indent=2)

print(f"[✔] Model saved to: {model_path}")


