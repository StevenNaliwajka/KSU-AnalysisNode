import pandas as pd
import re

from Codebase.DataManager.data_loader import DataLoader
from Codebase.Theoretical.solve import solve_rssi_from_m_t


def process_and_dump(output_csv="calculated_rssi.csv", target_depth=-3, target_instance=0):
    loader = DataLoader()

    # --- Load Soil ---
    soil_columns = {"soil temperature (°c)", "soil moisture value"}
    loader.load_data("soildata", instance_id=None, set_of_columns=soil_columns)
    soil_category = loader.data.get("soildata", {})
    if not soil_category:
        raise ValueError("No soil data found.")
    soil_instance_key = next(iter(soil_category.keys()))
    soil_instance_data = soil_category[soil_instance_key]

    # Grab all dataframes (with or without depth keys)
    soil_dataframes = []
    if "data" in soil_instance_data:
        soil_dataframes = soil_instance_data["data"]
    else:
        for subkey in soil_instance_data:
            if "data" in soil_instance_data[subkey]:
                soil_dataframes.extend(soil_instance_data[subkey]["data"])
    soil_df = pd.concat(soil_dataframes, ignore_index=True)

    # --- Load TVWS ---
    tvws_columns = {"drssi"}
    loader.load_data("tvwsdirt", instance_id=target_instance, set_of_columns=tvws_columns)
    tvws_category = loader.data.get("tvwsdirt", {})
    if not tvws_category:
        raise ValueError("No TVWS data found.")
    tvws_instance_key = next(iter(tvws_category.keys()))
    tvws_dataframes = []
    for subkey in tvws_category[tvws_instance_key]:
        if "data" in tvws_category[tvws_instance_key][subkey]:
            tvws_dataframes.extend(tvws_category[tvws_instance_key][subkey]["data"])
    tvws_df = pd.concat(tvws_dataframes, ignore_index=True)

    # --- Ensure datetime is parsed & drop nulls ---
    for df_name, df in [("soil", soil_df), ("tvws", tvws_df)]:
        before = len(df)
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
        df.dropna(subset=["datetime"], inplace=True)
        after = len(df)
        print(f"[INFO] {df_name}: removed {before - after} rows with invalid datetime.")

    # --- Merge on datetime (nearest within 1 minute) ---
    merged = pd.merge_asof(
        soil_df.sort_values("datetime"),
        tvws_df.sort_values("datetime"),
        on="datetime",
        direction="nearest",
        tolerance=pd.Timedelta("1min")
    ).dropna()

    print(f"[INFO] Merged dataset contains {len(merged)} rows after join.")

    # --- Rename for consistency ---
    merged.rename(columns={
        "soil temperature (°c)": "temp_c",
        "soil moisture value": "moisture_pct",
        "drssi": "mounted_rssi"
    }, inplace=True)

    # --- Compute RSSI ---
    merged["calculated_rssi"] = merged.apply(
        lambda row: solve_rssi_from_m_t(row["temp_c"], row["moisture_pct"], row["mounted_rssi"]),
        axis=1
    )

    # --- Save ---
    merged.to_csv(output_csv, index=False)
    print(f"[SUCCESS] Saved {len(merged)} rows to {output_csv}")


if __name__ == "__main__":
    process_and_dump()
