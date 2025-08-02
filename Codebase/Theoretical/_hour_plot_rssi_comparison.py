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
        return pd.to_datetime(combined, errors="coerce", utc=True)
    raise KeyError(f"Cannot build datetime. Columns available: {df.columns}")

def plot_rssi_comparison(tvws_path, calculated_csv):
    cutoff_date = pd.Timestamp("2025-06-15", tz="UTC")  # <-- date cutoff

    # --- Load all TVWS files directly ---
    tvws_files = list(pathlib.Path(tvws_path).glob("TVWSdirt_*.csv"))
    if not tvws_files:
        raise ValueError(f"No TVWS files found in {tvws_path}")

    tvws_dataframes = []
    for file in tvws_files:
        df = pd.read_csv(file, skiprows=2, header=0)
        df["datetime"] = build_datetime(df)
        df = df.dropna(subset=["datetime"])
        df = df[df["datetime"] <= cutoff_date]  # <-- filter by cutoff
        df["depth"] = extract_depth_from_filename(file.name)
        tvws_dataframes.append(df)

    tvws_df = pd.concat(tvws_dataframes, ignore_index=True)
    tvws_df = tvws_df.sort_values("datetime")

    # --- Load calculated RSSI CSV ---
    calc_df = pd.read_csv(calculated_csv)
    calc_df["datetime"] = pd.to_datetime(calc_df["datetime"], errors="coerce", utc=True)
    calc_df = calc_df.dropna(subset=["datetime"])
    calc_df = calc_df[calc_df["datetime"] <= cutoff_date]
    calc_df = calc_df.sort_values("datetime")

    # --- Merge (nearest within 1 min) ---
    merged = pd.merge_asof(
        tvws_df,
        calc_df[["datetime", "calculated_rssi"]],
        on="datetime",
        direction="nearest",
        tolerance=pd.Timedelta("1min")
    ).dropna()

    # --- Identify URSSI/DRSSI columns dynamically ---
    urssi_col = next((c for c in merged.columns if "urssi" in c.lower()), None)
    drssi_col = next((c for c in merged.columns if "drssi" in c.lower()), None)

    # --- Filter invalid RSSI values ---
    for col in [urssi_col, drssi_col, "calculated_rssi"]:
        if col and col in merged.columns:
            merged = merged[(merged[col] >= -100) & (merged[col] <= -40)]

    # --- Aggregate to hourly blocks ---
    merged.set_index("datetime", inplace=True)

    # Separate calculated_rssi
    calc_hourly = merged["calculated_rssi"].resample("1H").mean().reset_index()

    # Group by depth and resample sensor RSSI
    hourly = (
        merged.groupby("depth")
        .resample("1H")
        .mean(numeric_only=True)
        .reset_index()
    )

    # Merge hourly calculated RSSI back
    hourly = pd.merge_asof(
        hourly.sort_values("datetime"),
        calc_hourly.rename(columns={"calculated_rssi": "calculated_rssi_hourly"}),
        on="datetime",
        direction="nearest",
        tolerance=pd.Timedelta("1s")
    )

    # --- Colors by depth ---
    colors = {
        "0 inch": {"urssi": "blue", "drssi": "cyan"},
        "3 inch": {"urssi": "red", "drssi": "orange"},
        "Unknown": {"urssi": "gray", "drssi": "lightgray"}
    }

    # --- 1) Combined Plot ---
    plt.figure(figsize=(12, 6))
    for depth in hourly["depth"].unique():
        depth_data = hourly[hourly["depth"] == depth]
        if urssi_col:
            plt.scatter(depth_data["datetime"], depth_data[urssi_col], label=f"URSSI {depth}", alpha=0.8, s=30, c=colors.get(depth, {}).get("urssi", "gray"))
        if drssi_col:
            plt.scatter(depth_data["datetime"], depth_data[drssi_col], label=f"DRSSI {depth}", alpha=0.8, s=30, c=colors.get(depth, {}).get("drssi", "lightgray"))
    plt.scatter(hourly["datetime"], hourly["calculated_rssi"], label="Calculated RSSI", s=40, c="black")
    plt.xlabel("Time (Hourly)")
    plt.ylabel("RSSI (dBm)")
    plt.title("Hourly-Averaged URSSI & DRSSI vs Calculated RSSI")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    # --- 2–5) Individual comparisons (each signal vs Calculated RSSI) ---
    for depth in hourly["depth"].unique():
        for col, label in [(urssi_col, "URSSI"), (drssi_col, "DRSSI")]:
            if col:
                depth_data = hourly[hourly["depth"] == depth]
                plt.figure(figsize=(12, 6))
                plt.scatter(depth_data["datetime"], depth_data[col], label=f"{label} {depth}", alpha=0.8, s=30, c=colors.get(depth, {}).get(label.lower(), "gray"))
                plt.scatter(depth_data["datetime"], depth_data["calculated_rssi"], label="Calculated RSSI", s=40, c="black")
                plt.xlabel("Time (Hourly)")
                plt.ylabel("RSSI (dBm)")
                plt.title(f"Hourly-Averaged {label} {depth} vs Calculated RSSI")
                plt.legend()
                plt.grid()
                plt.tight_layout()
                plt.show()

if __name__ == "__main__":
    tvws_folder = r"C:\Users\steve\PycharmProjects\KSU-AnalysisNode\Data\Train\TVWS"
    calculated_csv = r"C:\Users\steve\PycharmProjects\KSU-AnalysisNode\Codebase\Theoretical\calculated_rssi.csv"
    plot_rssi_comparison(tvws_folder, calculated_csv)
