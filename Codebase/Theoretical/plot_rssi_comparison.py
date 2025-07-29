import pandas as pd
import matplotlib.pyplot as plt
import re
import pathlib

def extract_depth_from_filename(filename):
    match = re.search(r"tvwsdirt_(-?\d+)_", filename.lower())
    if match:
        depth = int(match.group(1))
        return f"{abs(depth)} inch"
    return "Unknown"

def build_datetime(df):
    """Build combined datetime column from Date + Time columns."""
    date_cols = [c for c in df.columns if "date" in c.lower()]
    time_cols = [c for c in df.columns if "time" in c.lower()]
    if date_cols and time_cols:
        combined = df[date_cols[0]].astype(str) + " " + df[time_cols[0]].astype(str)
        # Assume format like 6/6/2025 11:04:00
        return pd.to_datetime(combined, format="%m/%d/%Y %H:%M:%S", errors="coerce", utc=True)
    raise KeyError(f"Cannot build datetime. Columns available: {df.columns}")

def plot_rssi_comparison(tvws_path, calculated_csv):
    # --- Load all TVWS files ---
    tvws_files = list(pathlib.Path(tvws_path).glob("TVWSdirt_*.csv"))
    if not tvws_files:
        raise ValueError(f"No TVWS files found in {tvws_path}")

    tvws_dataframes = []
    for file in tvws_files:
        # --- Dynamically detect header row (find first row with "Date" and "Time") ---
        with open(file, 'r') as f:
            lines = f.readlines()

        header_row = None
        for i, line in enumerate(lines[:10]):  # only check first 10 lines
            if "Date" in line and "Time" in line:
                header_row = i
                break

        if header_row is None:
            raise ValueError(f"Could not detect header row in {file}")

        df = pd.read_csv(file, skiprows=header_row, header=0)

        df["datetime"] = build_datetime(df)
        df = df.dropna(subset=["datetime"])
        df["depth"] = extract_depth_from_filename(file.name)
        tvws_dataframes.append(df)

    tvws_df = pd.concat(tvws_dataframes, ignore_index=True)
    tvws_df = tvws_df.sort_values("datetime")

    # --- Load calculated RSSI CSV ---
    calc_df = pd.read_csv(calculated_csv)
    calc_df["datetime"] = pd.to_datetime(calc_df["datetime"], errors="coerce", utc=True)
    calc_df = calc_df.dropna(subset=["datetime"])
    calc_df = calc_df.sort_values("datetime")

    # --- Identify URSSI/DRSSI columns dynamically ---
    urssi_col = next((c for c in tvws_df.columns if "urssi" in c.lower()), None)
    drssi_col = next((c for c in tvws_df.columns if "drssi" in c.lower()), None)

    # --- Filter RSSI values between 0 and -40 dBm ---
    for col in [urssi_col, drssi_col]:
        if col and col in tvws_df.columns:
            tvws_df[col] = pd.to_numeric(tvws_df[col], errors="coerce")
            tvws_df = tvws_df[(tvws_df[col] <= -40) | (tvws_df[col] > 0)]

    # --- Keep only needed columns ---
    keep_cols = ["datetime", "depth"]
    if urssi_col: keep_cols.append(urssi_col)
    if drssi_col: keep_cols.append(drssi_col)
    tvws_df = tvws_df[keep_cols]

    # --- Resample TVWS to 1-hour averages per depth ---
    tvws_df.set_index("datetime", inplace=True)
    tvws_df = tvws_df.groupby(["depth", pd.Grouper(freq="1h")]).mean().reset_index()
    tvws_df = tvws_df.rename(columns={"datetime": "datetime"})
    tvws_df = tvws_df.sort_values("datetime")

    # --- Resample calculated RSSI to 1-hour averages ---
    calc_df.set_index("datetime", inplace=True)
    calc_df = calc_df.resample("1h").mean(numeric_only=True).reset_index()
    calc_df = calc_df.sort_values("datetime")

    # --- Merge with INNER JOIN on datetime (ensures alignment) ---
    merged = pd.merge(tvws_df, calc_df, on="datetime", how="inner")

    print(f"[DEBUG] TVWS hourly rows: {len(tvws_df)}")
    print(f"[DEBUG] Calculated RSSI hourly rows: {len(calc_df)}")
    print(f"[DEBUG] Merged rows: {len(merged)}")
    if merged.empty:
        raise ValueError("No merged data after hourly join — check time overlap.")

    # --- Colors by depth ---
    colors = {
        "0 inch": {"urssi": "blue", "drssi": "cyan"},
        "3 inch": {"urssi": "red", "drssi": "orange"},
        "Unknown": {"urssi": "gray", "drssi": "lightgray"}
    }

    # --- 1) Combined Plot ---
    plt.figure(figsize=(12, 6))
    for depth in merged["depth"].unique():
        depth_data = merged[merged["depth"] == depth]
        if urssi_col:
            plt.scatter(depth_data["datetime"], depth_data[urssi_col], label=f"URSSI {depth}", alpha=0.8, s=25, c=colors.get(depth, {}).get("urssi", "gray"))
        if drssi_col:
            plt.scatter(depth_data["datetime"], depth_data[drssi_col], label=f"DRSSI {depth}", alpha=0.8, s=25, c=colors.get(depth, {}).get("drssi", "lightgray"))
    plt.scatter(merged["datetime"], merged["calculated_rssi"], label="Calculated RSSI", s=30, c="black")
    plt.xlabel("Time")
    plt.ylabel("RSSI (dBm)")
    plt.title("All URSSI & DRSSI vs Calculated RSSI (Hourly Averages)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    # --- 2–5) Individual comparisons ---
    for depth in merged["depth"].unique():
        for col, label in [(urssi_col, "URSSI"), (drssi_col, "DRSSI")]:
            if col:
                depth_data = merged[merged["depth"] == depth]
                plt.figure(figsize=(12, 6))
                plt.scatter(depth_data["datetime"], depth_data[col], label=f"{label} {depth}", alpha=0.8, s=25, c=colors.get(depth, {}).get(label.lower(), "gray"))
                plt.scatter(depth_data["datetime"], depth_data["calculated_rssi"], label="Calculated RSSI", s=30, c="black")
                plt.xlabel("Time")
                plt.ylabel("RSSI (dBm)")
                plt.title(f"{label} {depth} vs Calculated RSSI (Hourly Averages)")
                plt.legend()
                plt.grid()
                plt.tight_layout()
                plt.show()

if __name__ == "__main__":
    tvws_folder = r"C:\Users\steve\PycharmProjects\KSU-AnalysisNode\Data\Train\TVWS"
    calculated_csv = r"C:\Users\steve\PycharmProjects\KSU-AnalysisNode\Codebase\Theoretical\calculated_rssi.csv"
    plot_rssi_comparison(tvws_folder, calculated_csv)
