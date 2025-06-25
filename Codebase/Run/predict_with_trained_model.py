import pandas as pd
import json
import traceback
from pathlib import Path
from datetime import datetime
from sklearn.metrics import mean_absolute_error, r2_score

from Codebase.CorrelationModeling.model_loader import load_model
from Codebase.DataManager.data_loader import DataLoader
from Codebase.Pathing.get_project_root import get_project_root
from Codebase.CorrelationModeling.prepare_training_data import detect_header_row, normalize_header, coalesce_columns

print("=== [Predict with Trained ML Model] ===\n")

loader = DataLoader()
project_root = get_project_root()
predict_dir = project_root / "Data" / "Predict"
model_dir = project_root / "Codebase" / "CorrelationModeling" / "MLBinary"

# === Prompt model selection ===
models = sorted(model_dir.glob("*.joblib"))
if not models:
    print("[✖] No trained models found.")
    exit(1)

print("[Available Models]:")
for i, m in enumerate(models, 1):
    print(f"[{i}] {m.name}")

choice = input("Select a model: ").strip()
try:
    model_path = models[int(choice) - 1]
except Exception:
    print("[✖] Invalid model selection.")
    exit(1)

# === Load model and metadata ===
model = load_model(str(model_path))
meta_path = model_path.with_suffix(".json")
if not meta_path.exists():
    print("[✖] Metadata JSON not found.")
    exit(1)

with open(meta_path) as f:
    metadata = json.load(f)

input_headers = [normalize_header(h) for h in metadata["inputs"]]
output_header = normalize_header(metadata["output"])

# === Load model and metadata ===
model = load_model(str(model_path))
meta_path = model_path.with_suffix(".json")
if not meta_path.exists():
    print("[✖] Metadata JSON not found.")
    exit(1)

with open(meta_path) as f:
    metadata = json.load(f)

# Normalize headers for internal consistency
input_headers = [normalize_header(h) for h in metadata["inputs"]]
output_header = normalize_header(metadata["output"])

print(f"\n[MODEL SELECTED]: {model_path.name}")
print(f"[METADATA LOADED FROM]: {meta_path.name}")
print(f"[INPUT HEADERS EXPECTED]:")
for raw, norm in zip(metadata["inputs"], input_headers):
    print(f"  - Raw: '{raw}'   →   Normalized: '{norm}'")

print(f"[OUTPUT HEADER EXPECTED]:")
print(f"  - Raw: '{metadata['output']}'   →   Normalized: '{output_header}'")


# === Load prediction data ===
print("\n[INFO] Scanning CSV files in Predict folder...")
csv_files = sorted(predict_dir.rglob("*.csv"))
used_headers = set()
files_to_merge = []

for f in csv_files:
    try:
        header_line, _ = detect_header_row(f)
        df = loader.read_csv(f, header_line=header_line)
        lower_cols = [normalize_header(c) for c in df.columns]

        print(f"\n[SCANNING FILE] {f.name}")
        # print(f"  Detected columns: {df.columns.tolist()}")

        # Detect datetime column
        if any('date' in col for col in lower_cols) and any('time' in col for col in lower_cols):
            date_col = df.columns[next(i for i, c in enumerate(lower_cols) if 'date' in c)]
            time_col = df.columns[next(i for i, c in enumerate(lower_cols) if 'time' in c)]
            df['datetime'] = pd.to_datetime(
                df[date_col].astype(str) + ' ' + df[time_col].astype(str),
                format="%Y-%m-%d %H-%M-%S",
                utc=True,
                errors='coerce'
            )
           # print(f"  Parsed datetime using: {date_col} + {time_col}")
        elif any('date' in col for col in lower_cols):
            date_col = df.columns[next(i for i, c in enumerate(lower_cols) if 'date' in c)]
            df["datetime"] = pd.to_datetime(df[date_col], utc=True, errors="coerce")
            #print(f"  Parsed datetime using: {date_col}")
        elif any('datetime' in col for col in lower_cols):
            dt_col = df.columns[next(i for i, c in enumerate(lower_cols) if 'datetime' in c)]
            df["datetime"] = pd.to_datetime(df[dt_col], utc=True, errors="coerce")
            #print(f"  Parsed datetime using: {dt_col}")
        else:
            print(f"  [WARN] No datetime column found. Skipping file.")
            continue

        df = df.dropna(subset=["datetime"])
        df["datetime"] = df["datetime"].dt.round("60s")

        # Match input/output columns
        available = [col for col in df.columns if normalize_header(col) in input_headers + [output_header]]
        matched = [normalize_header(col) for col in available]

        if matched:
            print(f"  Matched headers in this file: {matched}")
            used_headers.update(matched)
            files_to_merge.append(df[["datetime"] + available])
        else:
            print("  [INFO] No matching input/output headers found in this file.")

        if used_headers.issuperset(input_headers):
            print("  [✓] All required input headers found. Stopping early.")
            break

    except Exception as e:
        print(f"[ERROR] Loading {f.name}: {e}")
        traceback.print_exc()

if not files_to_merge:
    print("[✖] No usable files found for prediction.")
    exit(1)

print(f"\n[INFO] Merging {len(files_to_merge)} matching dataframes...")
expected_columns_lower = [col.lower() for col in input_headers + [output_header]]
merged_df = files_to_merge[0]

for i, df in enumerate(files_to_merge[1:], start=2):
    print(f"[DEBUG] File {i} time range: {df['datetime'].min()} → {df['datetime'].max()}")

    # Drop non-critical overlapping columns, but keep model inputs/outputs
    COLLISION_SAFE = ['datetime']
    cols_to_drop = [
        col for col in df.columns
        if col in merged_df.columns
        and col not in COLLISION_SAFE
        and normalize_header(col).lower() not in expected_columns_lower
        and not col.startswith('Unnamed')
    ]
    if cols_to_drop:
        print(f"[⚠️] Dropping overlapping non-critical columns before merge: {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)

    merged_df = pd.merge_asof(
        merged_df.sort_values("datetime"),
        df.sort_values("datetime"),
        on="datetime",
        direction="nearest",
        tolerance=pd.Timedelta(seconds=60),
        suffixes=('', f'_df{i}')
    )

# Coalesce duplicate versions of key columns (e.g., drssi, soil moisture value)
merged_df = coalesce_columns(merged_df)


# === Drop rows with missing input/output ===
print(f"\n[DEBUG] Rows before dropna: {len(merged_df)}")
drop_cols = input_headers + ([output_header] if output_header in merged_df.columns else [])
print(f"[DEBUG] Checking for missing values in: {drop_cols}")
print(merged_df[drop_cols].isnull().sum())

merged_df = merged_df.dropna(subset=drop_cols)
print(f"[DEBUG] Rows after dropna: {len(merged_df)}")

if merged_df.empty:
    print("[✖] No valid rows remaining for prediction.")
    exit(1)


# === Run Prediction ===
print(f"[INFO] Predicting on {len(merged_df)} rows...")
try:
    X = merged_df[input_headers]
    preds = model.predict(X)
    merged_df["prediction"] = preds

    if output_header in merged_df.columns:
        y_true = merged_df[output_header].values
        mae = mean_absolute_error(y_true, preds)
        r2 = r2_score(y_true, preds)
        print(f"[✔] Prediction complete. MAE = {mae:.4f}, R² = {r2:.4f}")
    else:
        print("[✔] Prediction complete (no ground truth to compare).")

    # Display sample output
    print(merged_df[["datetime"] + input_headers + ["prediction"] + ([output_header] if output_header in merged_df.columns else [])].head())

except Exception as e:
    print(f"[✖] Prediction failed: {e}")
    traceback.print_exc()
    exit(1)
