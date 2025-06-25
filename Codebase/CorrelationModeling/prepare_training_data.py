import pandas as pd
import logging
from collections import defaultdict

from Codebase.DataManager.Processing.DataMGMT.coalesce_columns import coalesce_columns
from Codebase.DataManager.Processing.Header.normalize_header import normalize_header
from Codebase.DataManager.Processing.detect_header_row import detect_header_row


def prepare_training_data(train_dir, loader, selected_headers, merge_tolerance, allowed_files=None):
    selected = [normalize_header(h) for h in selected_headers]
    print(f"\n[SELECTED HEADERS] {selected}")

    files = sorted(allowed_files) if allowed_files is not None else sorted(train_dir.rglob("*.csv"))
    print(f"[FILES TO PROCESS: {len(files)}] {[f.name for f in files]}")

    dfs = []
    header_counts = defaultdict(int)
    matched_files = []

    for f in files:
        print(f"\n[SCANNING FILE] {f.name}")
        skiprows, raw = detect_header_row(f)
        print(f"  Header detected at line {skiprows}: {raw}")
        try:
            df = loader.read_csv(f, header_line=skiprows)
            print(f"  CSV loaded successfully. Shape: {df.shape}")
        except Exception as e:
            logging.exception(f"[ERROR loading CSV] {f.name}: {e}")
            print(f"  Failed to read CSV: {e}")
            continue

        df.columns = [c.strip().replace('"', '').replace('’', "'") for c in df.columns]
        lower_cols = [normalize_header(c) for c in df.columns]

        # Detect datetime
        if any('date' in col for col in lower_cols) and any('time' in col for col in lower_cols):
            date_col = df.columns[next(i for i, col in enumerate(lower_cols) if 'date' in col)]
            time_col = df.columns[next(i for i, col in enumerate(lower_cols) if 'time' in col)]
            print(f"  Using columns for datetime: {date_col} + {time_col}")
            df['datetime'] = pd.to_datetime(
                df[date_col].astype(str) + ' ' + df[time_col].astype(str),
                format="%Y-%m-%d %H-%M-%S",  # <-- adjust this based on print output
                utc=True,
                errors='coerce'
            )
        elif any('date' in col for col in lower_cols):
            date_col = df.columns[next(i for i, col in enumerate(lower_cols) if 'date' in col)]
            print(f"  Using column for datetime: {date_col}")
            df['datetime'] = pd.to_datetime(df[date_col].astype(str), utc=True, errors='coerce')
        elif any('datetime' in col for col in lower_cols):
            dt_col = df.columns[next(i for i, col in enumerate(lower_cols) if 'datetime' in col)]
            print(f"  Using datetime column: {dt_col}")
            df['datetime'] = pd.to_datetime(df[dt_col].astype(str), utc=True, errors='coerce')
        else:
            print(f"  Skipping file. No valid datetime column found.")
            continue

        before = len(df)
        df = df.dropna(subset=['datetime'])
        dropped = before - len(df)
        print(f"  Dropped {dropped} rows without datetime")

        if df.empty:
            print(f"  Skipping file. No valid rows after datetime filtering.")
            continue

        df['datetime'] = df['datetime'].dt.round(f"{merge_tolerance}s")
        print(f"  Rounded datetime to nearest {merge_tolerance} seconds")

        # Match selected headers
        matches = []
        for i, col in enumerate(lower_cols):
            if col in selected:
                print(f"  Matched column: {df.columns[i]}")
                matches.append(df.columns[i])

        missing = [h for h in selected if h not in lower_cols]
        if missing:
            print(f"  Missing expected columns: {missing}")
        if not matches:
            print(f"  Skipping file. No selected headers found.")
            continue

        for col in matches:
            header_counts[normalize_header(col)] += 1
        matched_files.append((f.name, matches))

        slim = df[['datetime'] + matches].drop_duplicates('datetime').sort_values('datetime')
        print(f"  Loaded {len(slim)} unique rows from file")
        dfs.append(slim)

    print("\n[MATCHED FILES]")
    for name, cols in matched_files:
        print(f"  {name}: {cols}")

    print("\n[HEADER OCCURRENCES]")
    for h in selected:
        print(f"  {h}: found in {header_counts[h]} file(s)")

    if not dfs:
        raise ValueError("No valid files with datetime and matching headers.")

    print("\n[TIMESTAMP RANGES PER FILE]")
    for i, df in enumerate(dfs, start=1):
        print(f"  DF{i}: {df['datetime'].min()} → {df['datetime'].max()} ({len(df)} rows)")

    merged = dfs[0]
    print(f"\n[MERGING DATAFRAMES] Initial shape: {merged.shape}")

    for idx, df in enumerate(dfs[1:], start=2):
        before = merged.shape[0]

        # Ensure no duplicate columns (except 'datetime') before merging
        cols_to_drop = [col for col in df.columns if col in merged.columns and col != 'datetime']
        if cols_to_drop:
            print(f"  [⚠️] Dropping overlapping columns before merge: {cols_to_drop}")
            df = df.drop(columns=cols_to_drop)

        # Safe merge
        merged = pd.merge_asof(
            merged.sort_values('datetime'),
            df.sort_values('datetime'),
            on='datetime',
            tolerance=pd.Timedelta(seconds=merge_tolerance),
            direction='nearest',
            suffixes=('', f'_df{idx}')
        )

        after = merged.shape[0]
        print(f"  After merging DF{idx}: {before} → {after} rows")

    required = [c for c in merged.columns if normalize_header(c) in selected]
    pre_final = merged.shape[0]
    merged = merged.dropna(subset=required)
    merged = coalesce_columns(merged)

    print(f"\n[FINAL CLEANUP] Dropped {pre_final - merged.shape[0]} rows with missing required columns")
    print(f"  Final shape: {merged.shape}")

    print("\n[FINAL MERGED DATAFRAME PREVIEW]")
    print(merged.head(30).to_string(index=False))

    if merged.shape[0] < 2:
        raise ValueError("Not enough valid merged data for training.")

    return merged
