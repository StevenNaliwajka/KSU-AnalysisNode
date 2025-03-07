import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import matplotlib.dates as mdates

from Codebase.DataManager.data_loader import DataLoader


def snr_vs_moisture(tvws_num: int, moisture_num: int, dsnr_or_usnr: str, output_file:str) -> None:
    loader = DataLoader()
    caps_snr = dsnr_or_usnr.upper()
    tvws_instance = tvws_num

    loader.load_data("TVWSScenario", tvws_instance, {dsnr_or_usnr, "Date (Year-Mon-Day)", "Time (Hour-Min-Sec)"})
    snr_key = f"TVWSScenario_instance{tvws_instance}"

    moisture_instance = moisture_num
    loader.load_data("SoilData", moisture_instance,
                     {"Soil Moisture Value", "Date (Year-Mon-Day)", "Time (Hour-Min-Sec)"})
    moisture_key = f"SoilData_instance{moisture_instance}"

    if "TVWSScenario" not in loader.data or snr_key not in loader.data["TVWSScenario"]:
        print("No SNR data found.")
        return

    if "SoilData" not in loader.data or moisture_key not in loader.data["SoilData"]:
        print("No Soil Moisture data found.")
        return

    snr_df = pd.concat(loader.data["TVWSScenario"][snr_key]["data"])
    snr_df.columns = [col.strip().lower() for col in snr_df.columns]

    moisture_df = pd.concat(loader.data["SoilData"][moisture_key]["data"])
    moisture_df.columns = [col.strip().lower() for col in moisture_df.columns]

    snr_df["datetime"] = pd.to_datetime(snr_df["date (year-mon-day)"] + " " + snr_df["time (hour-min-sec)"],
                                        format="%Y-%m-%d %H-%M-%S", errors='coerce')
    moisture_df["datetime"] = pd.to_datetime(
        moisture_df["date (year-mon-day)"] + " " + moisture_df["time (hour-min-sec)"],
        format="%Y-%m-%d %H-%M-%S", errors='coerce')

    snr_df.dropna(subset=["datetime"], inplace=True)
    moisture_df.dropna(subset=["datetime"], inplace=True)

    snr_df[dsnr_or_usnr] = pd.to_numeric(snr_df[dsnr_or_usnr], errors='coerce')
    moisture_df["soil moisture value"] = pd.to_numeric(moisture_df["soil moisture value"], errors='coerce')

    merged_df = pd.merge_asof(snr_df.sort_values("datetime"), moisture_df.sort_values("datetime"), on="datetime")
    merged_df.dropna(subset=[dsnr_or_usnr, "soil moisture value"], inplace=True)

    if merged_df.empty:
        print("Warning: No valid data for correlation.")
        return

    def normalize(series):
        return (series - series.min()) / (series.max() - series.min()) if series.max() != series.min() else series

    merged_df[f"{dsnr_or_usnr}_norm"] = normalize(merged_df[dsnr_or_usnr])
    merged_df["soil_moisture_norm"] = normalize(merged_df["soil moisture value"])

    correlation_snr, _ = pearsonr(merged_df[f"{dsnr_or_usnr}_norm"], merged_df["soil_moisture_norm"])

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.scatter(merged_df["datetime"], merged_df[f"{dsnr_or_usnr}_norm"], color='r', label=f'{caps_snr} (Normalized)',
                alpha=0.6)
    ax2.scatter(merged_df["datetime"], merged_df["soil_moisture_norm"], color='g', label='Soil Moisture (Normalized)',
                alpha=0.6)

    ax1.set_xlabel('Timestamp', labelpad=15)
    ax1.set_ylabel(f'Normalized {caps_snr}', color='r')
    ax2.set_ylabel('Normalized Soil Moisture', color='g')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title(f'{caps_snr} vs. Soil Moisture\nCorrelation: {correlation_snr:.2f}')
    plt.xticks(rotation=45)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
    plt.tight_layout()
    plt.grid(True)

    output_path = output_file
    plt.savefig(output_path)
    print(f"Graph saved to {output_path}")


if __name__ == "__main__":
    args = sys.argv[1:]
    req_value = 3
    if len(args) < req_value:
        print(f"Error: Not enough arguments provided. Expected {req_value} values.")
        sys.exit(1)

    tvws_instance, moisture_instance, dsnr_or_usnr, out_path = args[:4]
    dsnr_or_usnr = dsnr_or_usnr.lower()
    snr_vs_moisture(int(tvws_instance), int(moisture_instance), dsnr_or_usnr, out_path)
