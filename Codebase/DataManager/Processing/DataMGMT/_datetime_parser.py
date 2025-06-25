import pandas as pd
#### WEIRD. WHEN ITS TIME TO FIX SPLIT_DATA. FIX
def parse_datetime(df):
    cols = [col.strip().lower() for col in df.columns]

    # Option 1: Combine date + time columns (e.g., Soil, TVWS)
    if "date (year-mon-day)" in cols and "time (hour-min-sec)" in cols:
        date_col = df.columns[cols.index("date (year-mon-day)")]
        time_col = df.columns[cols.index("time (hour-min-sec)")]
        time_str = df[time_col].astype(str).str.replace("-", ":", regex=False)
        combined = df[date_col].astype(str) + " " + time_str
        parsed = pd.to_datetime(combined, errors="coerce")
        print(f"[DEBUG] Parsed combined 'date + time' into datetime: {parsed.dropna().min()} to {parsed.dropna().max()}")
        return parsed

    # Option 2: Use 'simple date' (e.g., AmbientWeather)
    elif "simple date" in cols:
        simple_col = df.columns[cols.index("simple date")]
        parsed = pd.to_datetime(df[simple_col], errors="coerce")
        print(f"[DEBUG] Parsed 'simple date' into datetime: {parsed.dropna().min()} to {parsed.dropna().max()}")
        return parsed

    # Option 3: Auto-detect best column (fallback)
    for col in df.columns:
        try:
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().sum() > len(df) * 0.8:  # Accept if ≥80% valid
                print(f"[DEBUG] Fallback datetime parsing from column '{col}': {parsed.dropna().min()} to {parsed.dropna().max()}")
                return parsed
        except Exception:
            continue

    print("[ERROR] Failed to parse any datetime column.")
    return pd.Series(pd.NaT, index=df.index)
