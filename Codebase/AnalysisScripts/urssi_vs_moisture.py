import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import matplotlib.dates as mdates

from Codebase.DataLoader.data_loader import DataLoader


def urssi_vs_moisture(tvws_num:int, moisture_num:int) -> None:
    loader = DataLoader()

    tvws_instance = tvws_num
    # Load RSSI Data (Only URSSI)
    loader.load_data("TVWSScenario", tvws_instance, {"URSSI", "Date (Year-Mon-Day)", "Time (Hour-Min-Sec)"})
    rssi_key = f"TVWSScenario_instance{tvws_instance}"

    moisture_instance = moisture_num
    # Load Soil Moisture Data
    loader.load_data("SoilData", moisture_instance,
                     {"Soil Moisture Value", "Date (Year-Mon-Day)", "Time (Hour-Min-Sec)"})
    moisture_key = f"SoilData_instance{moisture_instance}"

    if "TVWSScenario" not in loader.data or rssi_key not in loader.data["TVWSScenario"]:
        print("No RSSI data found.")
        return

    if "SoilData" not in loader.data or moisture_key not in loader.data["SoilData"]:
        print("No Soil Moisture data found.")
        return

    # Extract RSSI data
    rssi_df = pd.concat(loader.data["TVWSScenario"][rssi_key]["data"])  # Combine all tables
    rssi_df.columns = [col.strip().lower() for col in rssi_df.columns]

    # Extract Soil Moisture data
    moisture_df = pd.concat(loader.data["SoilData"][moisture_key]["data"])  # Combine all tables
    moisture_df.columns = [col.strip().lower() for col in moisture_df.columns]

    # Convert RSSI Date & Time to datetime
    rssi_df["datetime"] = pd.to_datetime(rssi_df["date (year-mon-day)"] + " " + rssi_df["time (hour-min-sec)"],
                                         format="%Y-%m-%d %H-%M-%S", errors='coerce')

    # Convert Soil Moisture Date & Time to datetime
    moisture_df["datetime"] = pd.to_datetime(
        moisture_df["date (year-mon-day)"] + " " + moisture_df["time (hour-min-sec)"],
        format="%Y-%m-%d %H-%M-%S", errors='coerce')

    # Drop rows with invalid datetime values
    rssi_df.dropna(subset=["datetime"], inplace=True)
    moisture_df.dropna(subset=["datetime"], inplace=True)

    # Convert columns to numeric
    rssi_df["urssi"] = pd.to_numeric(rssi_df["urssi"], errors='coerce')
    moisture_df["soil moisture value"] = pd.to_numeric(moisture_df["soil moisture value"], errors='coerce')

    # Merge RSSI and Moisture data based on closest timestamps
    merged_df = pd.merge_asof(rssi_df.sort_values("datetime"), moisture_df.sort_values("datetime"), on="datetime")

    # Drop NaN values after merging
    merged_df.dropna(subset=["urssi", "soil moisture value"], inplace=True)

    # Ensure data is not empty before normalization
    if merged_df.empty:
        print("Warning: No valid data for correlation.")
        correlation_urssi = np.nan
    else:
        # Normalize Data
        def normalize(series):
            return (series - series.min()) / (series.max() - series.min()) if series.max() != series.min() else series

        merged_df["urssi_norm"] = normalize(merged_df["urssi"])
        merged_df["soil_moisture_norm"] = normalize(merged_df["soil moisture value"])

        # Check for valid correlation computation
        if merged_df["urssi_norm"].var() == 0 or merged_df["soil_moisture_norm"].var() == 0:
            print("Warning: Zero variance in one of the variables, correlation undefined.")
            correlation_urssi = np.nan
        else:
            correlation_urssi, _ = pearsonr(merged_df["urssi_norm"], merged_df["soil_moisture_norm"])

    # Plot Data using scatter plot
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.scatter(merged_df["datetime"], merged_df["urssi_norm"], color='r', label='URSSI (Normalized)', alpha=0.6)
    ax2.scatter(merged_df["datetime"], merged_df["soil_moisture_norm"], color='g', label='Soil Moisture (Normalized)',
                alpha=0.6)

    ax1.set_xlabel('Timestamp', labelpad=15)  # Adjust label padding to prevent cutoff
    ax1.set_ylabel('Normalized URSSI', color='r')
    ax2.set_ylabel('Normalized Soil Moisture', color='g')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title(f'URSSI vs. Soil Moisture\nCorrelation: {correlation_urssi:.2f}')
    plt.xticks(rotation=45)

    # Reduce timestamp clutter by setting date format and interval with two-line labels
    ax1.xaxis.set_major_locator(plt.MaxNLocator(5))  # Limit number of ticks
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))  # Two-line format
    plt.tight_layout()  # Adjust layout to prevent text cutoff
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    args = sys.argv[1:]

    req_value = 2
    if len(args) < req_value:
        print(f"Error: Not enough arguments provided. Expected {req_value} values.")
        sys.exit(1)
    tvws_instance, moisture_instance = map(int, args[:2])

    urssi_vs_moisture(tvws_instance, moisture_instance)
