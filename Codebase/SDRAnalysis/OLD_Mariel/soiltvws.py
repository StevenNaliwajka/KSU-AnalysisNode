import pandas as pd
import matplotlib.pyplot as plt
import glob
from dateutil import parser
import os
import subprocess

# ---- Remote machine info ----
remote_user = "tvws"
remote_host = "192.168.1.203"  # Pi IP address
remote_path = "/home/tvws/Documents/KSU-TowerNode/CSVOutput/*.csv"
local_soil_dir = "/opt/KSUFieldStation/DataCollection/SoilData"
save_dir = "./opt/KSUFieldStation/DataCollection/soil_csvs"

os.makedirs(save_dir, exist_ok=True)

# ---- Download soil files ----
scp_cmd = f"scp {remote_user}@{remote_host}:{remote_path} {local_soil_dir}/"
subprocess.run(scp_cmd, shell=True, check=True)


# ---------- Input Directories ----------
soil_dir = local_soil_dir        # <-- Change this to your soil CSV folder
tvws_dir = "/opt/TVWSDataScraper/CSVOutput"     # <-- Change this to your antenna CSV folder

# ---------- Utility Functions ----------
def safe_parse(dt):
    try:
        return parser.parse(str(dt)).replace(tzinfo=None)
    except Exception:
        return pd.NaT

def load_soil(files):
    dfs = []
    for f in files:
        df = pd.read_csv(f, skiprows=2, on_bad_lines='skip')
        df['timestamp'] = pd.to_datetime(
            df.iloc[:, 0] + ' ' + df.iloc[:, 1],
            format='%Y-%m-%d %H-%M-%S',
            errors='coerce',
            utc=True
        ).dt.tz_convert(None)
        df['soil_moisture'] = pd.to_numeric(df.iloc[:, 3], errors='coerce')
        df['soil_temperature'] = pd.to_numeric(df.iloc[:, 4], errors='coerce')
        dfs.append(df[['timestamp', 'soil_moisture', 'soil_temperature']])
    return pd.concat(dfs).dropna().sort_values('timestamp')


def verify_and_swap_tvws_roles(tvws_dir, snr_metric='DSNR'):
    files = sorted([f for f in os.listdir(tvws_dir) if f.endswith(".csv") and "TVWSScenario" in f])
    grouped = {}

    for f in files:
        key = "_".join(f.split("_")[2:])  # use timestamp part
        grouped.setdefault(key, []).append(f)

    for ts, pair in grouped.items():
        if len(pair) != 2:
            print(f"[!] Skipping unmatched pair: {pair}")
            continue

        f1 = next(f for f in pair if "instance1" in f)
        f2 = next(f for f in pair if "instance2" in f)
        p1 = os.path.join(tvws_dir, f1)
        p2 = os.path.join(tvws_dir, f2)

        try:
            df1 = pd.read_csv(p1, skiprows=2)
            df2 = pd.read_csv(p2, skiprows=2)

            mean1 = pd.to_numeric(df1[snr_metric], errors='coerce').mean()
            mean2 = pd.to_numeric(df2[snr_metric], errors='coerce').mean()

            if mean1 < mean2:
                print(f"↔ Swapping: {f1} ↔ {f2} (mean1={mean1:.2f} < mean2={mean2:.2f})")

                # Swap names by renaming
                temp = os.path.join(tvws_dir, "temp_swap.csv")
                os.rename(p1, temp)
                os.rename(p2, p1)
                os.rename(temp, p2)

        except Exception as e:
            print(f"Error processing {f1}, {f2}: {e}")


def load_tvws(files, metric):
    dfs = []
    for f in files:
        df = pd.read_csv(f, skiprows=2, on_bad_lines='skip')
        df['timestamp'] = pd.to_datetime(
            df.iloc[:, 0] + ' ' + df.iloc[:, 1],
            format='%Y-%m-%d %H-%M-%S',
            errors='coerce',
            utc=True
        ).dt.tz_convert(None)
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        df = df[df[metric] != 0]
        dfs.append(df[['timestamp', metric]])
    return pd.concat(dfs).dropna().sort_values('timestamp')


# ---------- File Discovery ----------
soil_files = glob.glob(os.path.join(soil_dir, "*.csv"))
tvws_files = glob.glob(os.path.join(tvws_dir, "*.csv"))

soil_instance1 = [f for f in soil_files if "instance1" in f]
soil_instance2 = [f for f in soil_files if "instance2" in f]
tvws_instance1 = [f for f in tvws_files if "instance1" in f]
tvws_instance2 = [f for f in tvws_files if "instance2" in f]

# ---------- Load and Save Soil ----------
soil1_df = load_soil(soil_instance1)
soil2_df = load_soil(soil_instance2)

soil1_df.to_csv(f"{save_dir}/soil_instance1_combined.csv", index=False)
soil2_df.to_csv(f"{save_dir}/soil_instance2_combined.csv", index=False)

verify_and_swap_tvws_roles(tvws_dir, snr_metric='USNR')

# ---------- Metrics to Plot ----------
metrics = ['DRSSI', 'URSSI', 'DSNR', 'USNR']
for metric in metrics:
    tvws1_df = load_tvws(tvws_instance1, metric)
    tvws2_df = load_tvws(tvws_instance2, metric)

    tvws1_df.to_csv(f"tvws_instance1_{metric}_combined.csv", index=False)
    tvws2_df.to_csv(f"tvws_instance2_{metric}_combined.csv", index=False)

    # Merge
    m1s1 = pd.merge_asof(tvws1_df, soil1_df, on='timestamp', direction='nearest', tolerance=pd.Timedelta('1s')).dropna()
    m2s1 = pd.merge_asof(tvws2_df, soil1_df, on='timestamp', direction='nearest', tolerance=pd.Timedelta('1s')).dropna()
    m1s2 = pd.merge_asof(tvws1_df, soil2_df, on='timestamp', direction='nearest', tolerance=pd.Timedelta('1s')).dropna()
    m2s2 = pd.merge_asof(tvws2_df, soil2_df, on='timestamp', direction='nearest', tolerance=pd.Timedelta('1s')).dropna()

    # Plot
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    sc1 = axs[0].scatter(
        m2s1[metric], m2s1['soil_moisture'],
        c=m2s1['soil_temperature'], cmap='viridis', alpha=0.6, label='Buried Rx'
    )
    axs[0].scatter(m1s1[metric], m1s1['soil_moisture'], color='red', alpha=0.6, label='Mounted Rx')
    axs[0].set_title(f'Soil 1 Moisture vs {metric}')
    axs[0].set_xlabel(f'{metric} (dBm or dB)')
    axs[0].set_ylabel('Soil Moisture (%)')
    axs[0].grid(True)
    axs[0].legend()

    sc2 = axs[1].scatter(
        m2s2[metric], m2s2['soil_moisture'],
        c=m2s2['soil_temperature'], cmap='viridis', alpha=0.6, label='Buried Rx'
    )
    axs[1].scatter(m1s2[metric], m1s2['soil_moisture'], color='red', alpha=0.6, label='Mounted Rx')
    axs[1].set_title(f'Soil 2 Moisture vs {metric}')
    axs[1].set_xlabel(f'{metric} (dBm or dB)')
    axs[1].set_ylabel('Soil Moisture (%)')
    axs[1].grid(True)
    axs[1].legend()

    fig.colorbar(sc1, ax=axs[0], label='Soil Temp (°C)')
    fig.colorbar(sc2, ax=axs[1], label='Soil Temp (°C)')

    plt.tight_layout()
    plt.savefig(f"soil_moisture_vs_{metric}.png")
    plt.show()

