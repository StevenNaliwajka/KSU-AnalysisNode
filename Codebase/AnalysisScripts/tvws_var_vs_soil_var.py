import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import matplotlib.dates as mdates

from Codebase.DataManager.data_loader import DataLoader

def tvws_var_vs_soil_var(tvws_num: int, moisture_num: int, var_1: str, var_2: str, output_path: str) -> None:
    loader = DataLoader()
    var_1_caps = var_1.upper()
    tvws_instance = tvws_num

    loader.load_data("TVWSScenario", tvws_instance, {var_1, "Date (Year-Mon-Day)", "Time (Hour-Min-Sec)"})
    var_1_key = f"TVWSScenario_instance{tvws_instance}"

    moisture_instance = moisture_num
    loader.load_data("SoilData", moisture_instance, {var_2, "Date (Year-Mon-Day)", "Time (Hour-Min-Sec)"})
    var_2_key = f"SoilData_instance{moisture_instance}"

    if "TVWSScenario" not in loader.data or var_1_key not in loader.data["TVWSScenario"]:
        print(f"No {var_1} data found.")
        return

    if "SoilData" not in loader.data or var_2_key not in loader.data["SoilData"]:
        print(f"No {var_2} data found.")
        return

    var_1_df = pd.concat(loader.data["TVWSScenario"][var_1_key]["data"])
    var_1_df.columns = [col.strip().lower() for col in var_1_df.columns]

    var_2_df = pd.concat(loader.data["SoilData"][var_2_key]["data"])
    var_2_df.columns = [col.strip().lower() for col in var_2_df.columns]

    var_1_df["datetime"] = pd.to_datetime(var_1_df["date (year-mon-day)"] + " " + var_1_df["time (hour-min-sec)"],
                                            format="%Y-%m-%d %H-%M-%S", errors='coerce')
    var_2_df["datetime"] = pd.to_datetime(
        var_2_df["date (year-mon-day)"] + " " + var_2_df["time (hour-min-sec)"],
        format="%Y-%m-%d %H-%M-%S", errors='coerce')

    var_1_df.dropna(subset=["datetime"], inplace=True)
    var_2_df.dropna(subset=["datetime"], inplace=True)

    var_1_df[var_1] = pd.to_numeric(var_1_df[var_1], errors='coerce')
    var_2_df[var_2] = pd.to_numeric(var_2_df[var_2], errors='coerce')

    merged_df = pd.merge_asof(var_1_df.sort_values("datetime"), var_2_df.sort_values("datetime"), on="datetime")
    merged_df.dropna(subset=[var_1, var_2], inplace=True)

    if merged_df.empty:
        print("Warning: No valid data for correlation.")
        return

    def normalize(series):
        return (series - series.min()) / (series.max() - series.min()) if series.max() != series.min() else series

    merged_df[f"{var_1}_norm"] = normalize(merged_df[var_1])
    merged_df[f"{var_2}_norm"] = normalize(merged_df[var_2])

    correlation, _ = pearsonr(merged_df[f"{var_1}_norm"], merged_df[f"{var_2}_norm"])

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.scatter(merged_df["datetime"], merged_df[f"{var_1}_norm"], color='r',
                label=f'{var_1_caps} (Normalized)', alpha=0.6)
    ax2.scatter(merged_df["datetime"], merged_df[f"{var_2}_norm"], color='g', label=f'{var_2} (Normalized)',
                alpha=0.6)

    ax1.set_xlabel('Timestamp', labelpad=15)
    ax1.set_ylabel(f'Normalized {var_1_caps}', color='r')
    ax2.set_ylabel(f'Normalized {var_2}', color='g')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title(f'{var_1_caps} vs. {var_2}\nCorrelation: {correlation:.2f}')
    plt.xticks(rotation=45)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
    plt.tight_layout()
    plt.grid(True)

    plt.savefig(output_path)
    print(f"Graph saved to {output_path}")

if __name__ == "__main__":
    args = sys.argv[1:]
    req_value = 5
    if len(args) < req_value:
        print(f"Error: Not enough arguments provided. Expected {req_value} values.")
        sys.exit(1)

    tvws_instance, moisture_instance, var_1, var_2, out_path = args[:5]
    var_1 = var_1.lower()
    var_2 = var_2.lower()
    tvws_var_vs_soil_var(int(tvws_instance), int(moisture_instance), var_1, var_2, out_path)
