from datetime import datetime, timezone
import json
import logging
import re
from pathlib import Path
from sklearn.utils import shuffle

from Codebase.CorrelationModeling.header_scanner import scan_unique_headers
from Codebase.CorrelationModeling.data_preparer import prepare_training_data
from Codebase.CorrelationModeling.PolyRegression.poly_train import train_model
from Codebase.CorrelationModeling.model_loader import save_model
from Codebase.DataManager.data_loader import DataLoader
from Codebase.Pathing.get_project_root import get_project_root

logging.basicConfig(filename="train_debug.log", level=logging.DEBUG)

def prompt_instance_selection(train_dir):
    def scan_by_type(type_keyword):
        results = {}
        for f in sorted(train_dir.rglob("*.csv")):
            if type_keyword in f.name.lower():
                match = re.search(r"instance(\d+)", f.name.lower())
                if match:
                    instance = int(match.group(1))
                    results.setdefault(instance, []).append(f)
        return results

    def prompt_user(type_name, instances):
        print(f"\n[{type_name.upper()} Instances Detected]")
        for inst, files in instances.items():
            print(f"[{inst}] ({len(files)} file(s))")
            for f in files:
                print(f"     - {f.name}")
        selected = input(f"Select {type_name} instance(s) (e.g., 1 or 1,2): ").strip()
        selected_ids = [int(i.strip()) for i in selected.split(",") if i.strip().isdigit()]
        selected_files = []
        for i in selected_ids:
            selected_files.extend(instances.get(i, []))
        return selected_files

    soil_instances = scan_by_type("soil")
    tvws_instances = scan_by_type("tvws")
    ambient_files = [f for f in train_dir.rglob("*.csv") if "ambient" in f.name.lower() or "weather" in f.name.lower()]

    selected_files = []
    if soil_instances:
        selected_files.extend(prompt_user("Soil", soil_instances))
    if tvws_instances:
        selected_files.extend(prompt_user("TVWS", tvws_instances))
    selected_files.extend(ambient_files)  # Always include ambient

    return selected_files


def main():
    print("=== [Train a New ML Model] ===")

    loader = DataLoader()
    project_root = get_project_root()
    train_dir = project_root / "Data" / "Train"
    config_path = project_root / "Codebase" / "CorrelationModeling" / "merge_config.json"

    if not config_path.exists():
        print(f"[✖] Missing config file: {config_path}")
        return

    merge_tolerance = int(json.load(open(config_path)).get("merge_tolerance_seconds", 60))

    # Prompt file selection first so we only scan relevant headers
    allowed_files = prompt_instance_selection(train_dir)

    col_id_map, header_sources = scan_unique_headers(train_dir, loader, files_to_scan=allowed_files)

    for i, col in col_id_map.items():
        print(f"[{i}] {col}")

    input_ids = input("Select input columns (e.g., 2,3): ").split(",")
    output_id = input("Select output column (e.g., 1): ").strip()

    try:
        input_cols = [col_id_map[i.strip()] for i in input_ids]
        output_col = col_id_map[output_id]
    except KeyError:
        print("[✖] Invalid selection")
        return

    df = prepare_training_data(train_dir, loader, input_cols + [output_col], merge_tolerance, allowed_files=allowed_files)

    print(f"[INFO] Final merged DataFrame has {df.shape[0]} rows and {df.shape[1]} columns")
    print("[INFO] Merged headers:")
    for col in df.columns:
        print(f"  - {col}")

    df = df.dropna()
    df = df.rename(columns={"datetime": "time"})
    df = df[["time"] + input_cols + [output_col]]
    df = shuffle(df)

    print(f"[INFO] Training on shape: {df.shape}")
    degree = int(input("Enter polynomial degree [default=2]: ") or 2)
    model, score = train_model(df, input_cols, output_col, degree)
    print(f"[✔] Model R²: {score:.3f}")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    model_dir = project_root / "Codebase" / "CorrelationModeling" / "MLBinary"
    model_path = model_dir / f"model_{timestamp}.joblib"
    model_dir.mkdir(exist_ok=True)

    save_model(model, str(model_path))

    metadata = {
        "inputs": input_cols,
        "output": output_col,
        "degree": degree
    }
    with open(model_path.with_suffix(".json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"[✔] Model + metadata saved at {model_path}")


if __name__ == "__main__":
    main()
