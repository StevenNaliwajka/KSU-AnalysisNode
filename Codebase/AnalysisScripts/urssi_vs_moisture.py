import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

from Codebase.DataLoader.data_loader import DataLoader


def urssi_vs_moisture():
    loader = DataLoader()

    # Load RSSI Data (Only URSSI)
    loader.load_data("TVWSScenario", 1, {"URSSI", "Date (Mon/Day/Year)", "Time (Hour:Min:Sec)"})
    rssi_key = "TVWSScenario_instance1"

    # Load Soil Moisture Data
    loader.load_data("SoilData", 1, {"Soil Moisture Value", "Timestamp"})
    moisture_key = "SoilData_instance1"

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
    rssi_df["datetime"] = pd.to_datetime(rssi_df["date (mon/day/year)"] + " " + rssi_df["time (hour:min:sec)"],
                                         format="%m/%d/%Y %H:%M:%S", errors='coerce')

    # Convert Soil Moisture Timestamp to datetime
    moisture_df["datetime"] = pd.to_datetime(moisture_df["timestamp"], format="%m-%d-%Y-%H-%M", errors='coerce')

    # Drop rows with invalid datetime values
    rssi_df.dropna(subset=["datetime"], inplace=True)
    moisture_df.dropna(subset=["datetime"], inplace=True)

    # Ensure datetime dtype consistency
    rssi_df["datetime"] = pd.to_datetime(rssi_df["datetime"])
    moisture_df["datetime"] = pd.to_datetime(moisture_df["datetime"])

    # Convert columns to numeric
    def normalize(series):
        return (series - series.min()) / (series.max() - series.min())

    rssi_df["urssi"] = pd.to_numeric(rssi_df["urssi"], errors='coerce').fillna(0)
    moisture_df["soil moisture value"] = pd.to_numeric(moisture_df["soil moisture value"], errors='coerce').fillna(0)

    # Merge RSSI and Moisture data based on closest timestamps
    merged_df = pd.merge_asof(rssi_df.sort_values("datetime"), moisture_df.sort_values("datetime"), on="datetime")

    # Normalize Data
    merged_df["urssi_norm"] = normalize(merged_df["urssi"])
    merged_df["soil_moisture_norm"] = normalize(merged_df["soil moisture value"])

    # Compute correlation
    correlation_urssi, _ = pearsonr(merged_df["urssi_norm"], merged_df["soil_moisture_norm"])

    # Plot Data
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(merged_df["datetime"], merged_df["urssi_norm"], 'r-', label='URSSI (Normalized)')
    ax2.plot(merged_df["datetime"], merged_df["soil_moisture_norm"], 'g-', label='Soil Moisture (Normalized)')

    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Normalized URSSI', color='r')
    ax2.set_ylabel('Normalized Soil Moisture', color='g')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title(f'URSSI vs. Soil Moisture\nCorrelation: {correlation_urssi:.2f}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()


# Usage Example
if __name__ == "__main__":
    urssi_vs_moisture()