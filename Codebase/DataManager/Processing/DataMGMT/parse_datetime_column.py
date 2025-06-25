from Codebase.DataManager.Processing.Header.detect_header_row import detect_header_row
import pandas as pd

def parse_datetime_column(csv_path: str, df: pd.DataFrame) -> pd.Series:
    header_row_idx, header_cols = detect_header_row(csv_path)

    # Drop rows above the actual header
    df = df.iloc[header_row_idx:].reset_index(drop=True)
    df.columns = header_cols

    cols = [col.strip().lower() for col in df.columns]

    # Combined date + time (used for Soil & TVWS)
    if "date (year-mon-day)" in cols and "time (hour-min-sec)" in cols:
        date_col = df.columns[cols.index("date (year-mon-day)")]
        time_col = df.columns[cols.index("time (hour-min-sec)")]
        combined = (
            df[date_col].astype(str).str.strip() + " " +
            df[time_col].astype(str).str.strip().str.replace("-", ":", regex=False)
        )
        parsed = pd.to_datetime(combined, errors="coerce", utc=True)
        print(f"[DEBUG] Parsed combined datetime in {csv_path}: {parsed.notna().sum()} rows valid")
        return parsed

    # Simple date fallback
    elif "simple date" in cols:
        col = df.columns[cols.index("simple date")]
        parsed = pd.to_datetime(df[col], errors="coerce", utc=True)
        print(f"[DEBUG] Parsed simple datetime in {csv_path}: {parsed.notna().sum()} rows valid")
        return parsed

    # Generic fallback — try each column
    for col in df.columns:
        try:
            parsed = pd.to_datetime(df[col], errors="coerce", utc=True)
            if parsed.notna().sum() > 0.8 * len(parsed):
                print(f"[DEBUG] Parsed fallback datetime in {csv_path}: {parsed.notna().sum()} rows valid")
                return parsed
        except Exception:
            continue

    print(f"[ERROR] Could not parse datetime in {csv_path}")
    return pd.Series(pd.NaT, index=df.index)
