import pandas as pd
from pathlib import Path
from Codebase.DataManager.data_loader import DataLoader
from Codebase.Pathing.get_project_root import get_project_root

def is_time_col(colname):
    colname = colname.lower()
    return "date" in colname or "time" in colname or colname in ("datetime",)

def main():
    project_root = get_project_root()
    data_dir = project_root / "Data" / "Train"
    loader = DataLoader()

    soil_files = sorted(data_dir.rglob("SoilData_*.csv"))
    results = []

    print("=== Soil File Header Scan ===")
    for file in soil_files:
        try:
            df = loader.read_csv(file, skip_rows=2)
            original_shape = df.shape

            if "Date" in df.columns and "Time" in df.columns:
                df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], utc=True, errors='coerce')
            elif "Date" in df.columns:
                df["datetime"] = pd.to_datetime(df["Date"], utc=True, errors='coerce')
            else:
                df["datetime"] = pd.to_datetime(df.iloc[:, 0], utc=True, errors='coerce')

            df = df.dropna(subset=["datetime"])

            valid_headers = [col for col in df.columns if not is_time_col(col)]

            for header in valid_headers:
                nonnull_count = df[header].dropna().shape[0]
                results.append({
                    "file": file.name,
                    "header": header,
                    "nonnull_rows": nonnull_count,
                })

        except Exception as e:
            print(f"[ERROR] {file.name}: {e}")

    # Sort by count, descending
    results = sorted(results, key=lambda x: x["nonnull_rows"], reverse=True)

    print("\n=== Ranked Headers by Row Count ===")
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['file']} — {r['header']}: {r['nonnull_rows']} rows")

if __name__ == "__main__":
    main()
