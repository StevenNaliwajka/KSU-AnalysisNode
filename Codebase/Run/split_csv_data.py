import pandas as pd
from pathlib import Path
import argparse
from Codebase.Pathing.get_project_root import get_project_root

DATA_ROOT = get_project_root() / "Data"
TRAIN_DIR = DATA_ROOT / "Train"
PREDICT_DIR = DATA_ROOT / "Predict"
FOLDERS = ["Atmospheric", "SDR", "Soil", "TVWS"]

def ensure_predict_subfolder(folder_name):
    dest_dir = PREDICT_DIR / folder_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    return dest_dir

def detect_data_start(filepath, folder):
    if folder == "Atmospheric":
        return 1
    elif folder in {"Soil", "TVWS"}:
        return 3
    else:
        return 1

def parse_datetime_column(df, folder):
    if folder == "Atmospheric":
        df["datetime"] = pd.to_datetime(df[0], utc=True, errors="coerce")
    elif folder in {"Soil", "TVWS"}:
        df["datetime"] = pd.to_datetime(df[0].astype(str) + " " + df[1].astype(str), format="%Y-%m-%d %H-%M-%S", utc=True, errors="coerce")
    else:
        df["datetime"] = pd.to_datetime(df[0], utc=True, errors="coerce")
    return df.dropna(subset=["datetime"])

def split_by_time(df, train_cutoff):
    df_train = df[df["datetime"] < train_cutoff].copy()
    df_predict = df[df["datetime"] >= train_cutoff].copy()
    return df_train, df_predict

def split_csv(filepath, folder, train_cutoff):
    data_start_line = detect_data_start(filepath, folder)
    df = pd.read_csv(filepath, skiprows=data_start_line, header=None)
    with open(filepath, 'r', encoding='utf-8') as f:
        headers = [next(f) for _ in range(data_start_line)]

    if len(df) < 2:
        print(f"[⚠️] Skipping {filepath.name} due to insufficient rows.")
        return

    df = parse_datetime_column(df, folder)
    if df.empty:
        print(f"[⚠️] Skipping {filepath.name} due to no valid datetime rows.")
        return

    df_train, df_predict = split_by_time(df, train_cutoff)

    # Overwrite Train file
    df_train.drop(columns=["datetime"]).to_csv(filepath, index=False, header=False)
    with open(filepath, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0)
        f.writelines(headers)
        f.write(content)

    # Write Predict file
    dest = ensure_predict_subfolder(folder) / filepath.name
    df_predict.drop(columns=["datetime"]).to_csv(dest, index=False, header=False)
    with open(dest, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0)
        f.writelines(headers)
        f.write(content)

    print(f"[✅] {filepath.name} — Train: {len(df_train)}, Predict: {len(df_predict)}")

def main(train_ratio):
    print(f"\n📂 Starting aligned time-based split ({int(train_ratio*100)}% train / {int((1-train_ratio)*100)}% predict)\n")

    all_datetimes = []

    # Step 1: Collect global datetime range
    for folder in FOLDERS:
        folder_path = TRAIN_DIR / folder
        if not folder_path.exists():
            continue
        for file in folder_path.glob("*.csv"):
            data_start_line = detect_data_start(file, folder)
            try:
                df = pd.read_csv(file, skiprows=data_start_line, header=None)
                df = parse_datetime_column(df, folder)
                all_datetimes.extend(df["datetime"].tolist())
            except Exception as e:
                print(f"[⚠️] Failed reading {file.name}: {e}")

    if not all_datetimes:
        print("[✖] No valid datetime values found across any files.")
        return

    all_datetimes = sorted(all_datetimes)
    train_cutoff = all_datetimes[int(len(all_datetimes) * train_ratio)]
    print(f"[INFO] Train cutoff timestamp: {train_cutoff}\n")

    # Step 2: Apply time-based split to all files
    for folder in FOLDERS:
        folder_path = TRAIN_DIR / folder
        if not folder_path.exists():
            print(f"[⚠️] Folder not found: {folder}")
            continue
        for file in sorted(folder_path.glob("*.csv")):
            split_csv(file, folder, train_cutoff)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split CSV files into train and predict sets, aligned by time.")
    parser.add_argument("--train_ratio", type=float, default=0.8, help="Ratio of data to keep in training set")
    args = parser.parse_args()

    main(train_ratio=args.train_ratio)
