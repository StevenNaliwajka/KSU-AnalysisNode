import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import matplotlib.dates as mdates

from Codebase.DataManager.data_loader import DataLoader


def rssi_vs_moisture(tvws_num: int, moisture_num: int, drssi_or_urssi: str, output_path:str) -> None:
    loader = DataLoader()
    rssi_caps = drssi_or_urssi.upper()
    tvws_instance = tvws_num

    loader.load_data("TVWSScenario", tvws_instance, {drssi_or_urssi, "Date (Year-Mon-Day)", "Time (Hour-Min-Sec)"})
    rssi_key = f"TVWSScenario_instance{tvws_instance}"

    moisture_instance = moisture_num
    loader.load_data("SoilData", moisture_instance,
                     {"Soil Moisture Value", "Date (Year-Mon-Day)", "Time (Hour-Min-Sec)"})
    moisture_key = f"SoilData_instance{moisture_instance}"

    if "TVWSScenario" not in loader.data or rssi_key not in loader.data["TVWSScenario"]:
        print("No RSSI data found.")
        return

    if "SoilData" not in loader.data or moisture_key not in loader.data["SoilData"]:
        print("No Soil Moisture data found.")
        return

    rssi_df = pd.concat(loader.data["TVWSScenario"][rssi_key]["data"])
    rssi_df.columns = [col.strip().lower() for col in rssi_df.columns]

    moisture_df = pd.concat(loader.data["SoilData"][moisture_key]["data"])
    moisture_df.columns = [col.strip().lower() for col in moisture_df.columns]

    rssi_df["datetime"] = pd.to_datetime(rssi_df["date (year-mon-day)"] + " " + rssi_df["time (hour-min-sec)"],
                                         format="%Y-%m-%d %H-%M-%S", errors='coerce')
    moisture_df["datetime"] = pd.to_datetime(
        moisture_df["date (year-mon-day)"] + " " + moisture_df["time (hour-min-sec)"],
        format="%Y-%m-%d %H-%M-%S", errors='coerce')

    rssi_df.dropna(subset=["datetime"], inplace=True)
    moisture_df.dropna(subset=["datetime"], inplace=True)

    rssi_df[drssi_or_urssi] = pd.to_numeric(rssi_df[drssi_or_urssi], errors='coerce')
    moisture_df["soil moisture value"] = pd.to_numeric(moisture_df["soil moisture value"], errors='coerce')

    merged_df = pd.merge_asof(rssi_df.sort_values("datetime"), moisture_df.sort_values("datetime"), on="datetime")
    merged_df.dropna(subset=[drssi_or_urssi, "soil moisture value"], inplace=True)

    if merged_df.empty:
        print("Warning: No valid data for correlation.")
        return

    def normalize(series):
        return (series - series.min()) / (series.max() - series.min()) if series.max() != series.min() else series

    merged_df[f"{drssi_or_urssi}_norm"] = normalize(merged_df[drssi_or_urssi])
    merged_df["soil_moisture_norm"] = normalize(merged_df["soil moisture value"])

    correlation_rssi, _ = pearsonr(merged_df[f"{drssi_or_urssi}_norm"], merged_df["soil_moisture_norm"])

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.scatter(merged_df["datetime"], merged_df[f"{drssi_or_urssi}_norm"], color='r',
                label=f'{rssi_caps} (Normalized)', alpha=0.6)
    ax2.scatter(merged_df["datetime"], merged_df["soil_moisture_norm"], color='g', label='Soil Moisture (Normalized)',
                alpha=0.6)

    ax1.set_xlabel('Timestamp', labelpad=15)
    ax1.set_ylabel(f'Normalized {rssi_caps}', color='r')
    ax2.set_ylabel('Normalized Soil Moisture', color='g')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title(f'{rssi_caps} vs. Soil Moisture\nCorrelation: {correlation_rssi:.2f}')
    plt.xticks(rotation=45)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
    plt.tight_layout()
    plt.grid(True)

    output_path = output_path
    plt.savefig(output_path)
    print(f"Graph saved to {output_path}")


if __name__ == "__main__":
    args = sys.argv[1:]
    req_value = 4
    if len(args) < req_value:
        print(f"Error: Not enough arguments provided. Expected {req_value} values.")
        sys.exit(1)

    tvws_instance, moisture_instance, drssi_or_urssi, out_path = args[:4]
    drssi_or_urssi = drssi_or_urssi.lower()
    rssi_vs_moisture(int(tvws_instance), int(moisture_instance), drssi_or_urssi, out_path)
