import pandas as pd
import logging

def scan_unique_headers(train_dir, loader, files_to_scan=None):
    header_sources = {}
    col_id_map = {}
    col_id = 1

    files = files_to_scan if files_to_scan is not None else sorted(train_dir.rglob("*.csv"))

    for f in files:
        try:
            header_line = 2 if "ambient-weather" not in f.name.lower() else 1
            df = loader.read_csv(f, header_line=header_line)

            if "date" in df.columns and "time" in df.columns:
                df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], utc=True, errors='coerce')
            elif "date" in df.columns:
                df["datetime"] = pd.to_datetime(df["date"], utc=True, errors='coerce')
            else:
                df["datetime"] = pd.to_datetime(df.iloc[:, 0], utc=True, errors='coerce')

            for col in df.columns:
                if col.lower().startswith("date") or col.lower().startswith("time") or col == "datetime":
                    continue
                if col not in header_sources:
                    header_sources[col] = f
                    col_id_map[str(col_id)] = col
                    col_id += 1

        except Exception as e:
            logging.exception(f"[Header Scan Error] {f.name}: {e}")

    return col_id_map, header_sources
