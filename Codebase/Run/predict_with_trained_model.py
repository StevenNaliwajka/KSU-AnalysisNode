import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from Codebase.CorrelationModeling.model_loader import load_model
from Codebase.DataManager.data_loader import DataLoader
from Codebase.Pathing.get_project_root import get_project_root
from sklearn.metrics import mean_absolute_error, r2_score
import traceback

print("=== [Predict with Trained ML Model] ===\n")

loader = DataLoader()
project_root = get_project_root()
predict_dir = project_root / "Data" / "Predict"
model_dir = project_root / "Codebase" / "CorrelationModeling" / "MLBinary"

# === Prompt user for model selection ===
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

# Load model and metadata
model = load_model(str(model_path))
meta_path = model_path.with_suffix(".json")
if not meta_path.exists():
    print("[✖] Metadata JSON not found.")
    exit(1)

with open(meta_path) as f:
    metadata = json.load(f)

input_headers = metadata["inputs"]
output_header = metadata["output"]

# === Load Predict Data ===
print("[INFO] Loading prediction data...")
csv_files = sorted(predict_dir.rglob("*.csv"))
used_headers = set()
files_to_merge = []

for f in csv_files:
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
        available = [col for col in input_headers + [output_header] if col in df.columns and col not in used_headers]
        if available:
            used_headers.update(available)
            files_to_merge.append(df[["datetime"] + available])

        if used_headers.issuperset(input_headers):
            break

    except Exception as e:
        print(f"[ERROR] Loading {f.name}: {e}")
        traceback.print_exc()

if not files_to_merge:
    print("[✖] No usable files found for prediction.")
    exit(1)

# === Merge and Predict ===
merged_df = files_to_merge[0]
for df in files_to_merge[1:]:
    merged_df = pd.merge(merged_df, df, on="datetime", how="outer")

# Drop rows with missing input or output data
print(f"[DEBUG] Rows before dropna: {len(merged_df)}")
drop_cols = input_headers + ([output_header] if output_header in merged_df.columns else [])
merged_df = merged_df.dropna(subset=drop_cols)
print(f"[DEBUG] Rows after dropna: {len(merged_df)}")

if merged_df.empty:
    print("[✖] No valid data rows remaining after dropping NaNs.")
    exit(1)

print(f"[INFO] Predicting on {len(merged_df)} rows...")

try:
    X = merged_df[input_headers]
    preds = model.predict(X)
    merged_df["prediction"] = preds

    if output_header in merged_df.columns:
        truth = merged_df[output_header].values
        mae = mean_absolute_error(truth, preds)
        r2 = r2_score(truth, preds)
        print(f"[✔] Prediction complete. MAE = {mae:.4f}, R² = {r2:.4f}")
    else:
        print("[✔] Prediction complete (no ground truth to compare).")

    # Display sample
    print(merged_df[["datetime"] + input_headers + ["prediction"] + ([output_header] if output_header in merged_df.columns else [])].head())

except Exception as e:
    print(f"[✖] Prediction failed: {e}")
    traceback.print_exc()
    exit(1)
