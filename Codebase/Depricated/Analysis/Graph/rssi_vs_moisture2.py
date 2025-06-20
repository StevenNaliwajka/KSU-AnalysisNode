import sys
import pandas as pd
import matplotlib.pyplot as plt

from Codebase.DataManager.old_data_loader import DataLoader


def rssi_vs_moisture2(tvws_num: int, moisture_num: int, drssi_or_urssi: str, output_path:str) -> None:
    loader = DataLoader()
    tvws_instance = tvws_num

    loader.load_data("TVWSScenario", tvws_instance, {drssi_or_urssi, "date (year-mon-day)", "time (hour-min-sec)"})
    rssi_key = f"TVWSScenario_instance{tvws_instance}"

    moisture_instance = moisture_num
    loader.load_data("SoilData", moisture_instance,
                     {"Soil Moisture Value", "date (year-mon-day)", "time (hour-min-sec)"})
    moisture_key = f"SoilData_instance{moisture_instance}"

    if "TVWSScenario" not in loader.data or rssi_key not in loader.data["TVWSScenario"]:
        print("No RSSI data found.")
        return

    if "SoilData" not in loader.data or moisture_key not in loader.data["SoilData"]:
        print("No Soil Moisture data found.")
        return

    rssi_df = pd.concat(loader.data["TVWSScenario"].get(rssi_key, {"data": []})["data"], ignore_index=True)
    rssi_df.columns = rssi_df.columns.str.strip().str.lower()

    rssi_df["timestamp"] = pd.to_datetime(
        rssi_df["date (year-mon-day)"].astype(str).str.strip() + " " +
        rssi_df["time (hour-min-sec)"].astype(str).str.strip(),
        format="%Y-%m-%d %H-%M-%S",
        errors="coerce"
    )
    rssi_df = rssi_df.dropna(subset=["timestamp"])
    rssi_df = rssi_df[["timestamp", drssi_or_urssi]]
    rssi_df.set_index("timestamp", inplace=True)

    moisture_df = pd.concat(loader.data["SoilData"].get(moisture_key, {"data": []})["data"], ignore_index=True)
    moisture_df.columns = moisture_df.columns.str.strip().str.lower()

    moisture_df["timestamp"] = pd.to_datetime(
        moisture_df["date (year-mon-day)"].astype(str).str.strip() + " " +
        moisture_df["time (hour-min-sec)"].astype(str).str.strip(),
        format="%Y-%m-%d %H-%M-%S",
        errors="coerce"
    )
    moisture_df = moisture_df.dropna(subset=["timestamp"])
    moisture_df = moisture_df[["timestamp", "soil moisture value"]]
    moisture_df.set_index("timestamp", inplace=True)

    merged_df = pd.merge_asof(
        rssi_df.sort_index(), moisture_df.sort_index(), left_index=True, right_index=True, direction="nearest"
    )

    if merged_df.empty:
        print("Error: No matching timestamps found between RSSI and Moisture data.")
        return

    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.set_xlabel("Timestamp")
    ax1.set_ylabel("RSSI (dB)", color="tab:blue")
    ax1.plot(merged_df.index, merged_df[drssi_or_urssi], label="RSSI", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Soil Moisture Value", color="tab:green")
    ax2.plot(merged_df.index, merged_df["soil moisture value"], label="Moisture", color="tab:green", linestyle="dashed")
    ax2.tick_params(axis="y", labelcolor="tab:green")

    fig.autofmt_xdate()
    plt.title(f"RSSI vs Soil Moisture (TVWS {tvws_num}, Moisture Sensor {moisture_num})")
    plt.legend(loc="best")

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
    rssi_vs_moisture2(int(tvws_instance), int(moisture_instance), drssi_or_urssi, out_path)
