import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from dateutil import parser

# ---------- Configuration ----------
soil_dir = "/opt/KSUFieldStation/DataCollection/SoilData"
tvws_dir = "/opt/TVWSDataScraper/CSVOutput"

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

# ---------- Load Data ----------
soil1_df = load_soil(soil_instance1)
soil2_df = load_soil(soil_instance2)

# ---------- Plot Time Series ----------
metrics = ['DRSSI', 'URSSI']
fig, axs = plt.subplots(len(metrics), 1, figsize=(14, 12), sharex=True)

for i, metric in enumerate(metrics):
    tvws1_df = load_tvws(tvws_instance1, metric)
    tvws2_df = load_tvws(tvws_instance2, metric)

    ax1 = axs[i]
    ax1.scatter(tvws1_df['timestamp'], tvws1_df[metric], label=f'TVWS 1 (Mounted) {metric}', color='blue', alpha=0.6, s=8)
    ax1.scatter(tvws2_df['timestamp'], tvws2_df[metric], label=f'TVWS 2 (Buried: 3") {metric}', color='red', alpha=0.6, s=8)
    ax1.set_ylabel(f"{metric} (dBm)")
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(soil1_df['timestamp'], soil1_df['soil_temperature'], label='Soil Sensor 1: 1"', color='green')#, alpha=0.5, s=100)
    ax2.plot(soil2_df['timestamp'], soil2_df['soil_temperature'], label='Soil Sensor 2: 3"', color='orange')#, alpha=0.5, s=100)
    ax2.set_ylabel('Temperature (C)')
    axs[i].minorticks_on()
    axs[i].grid(True, which='major', linestyle='-', linewidth=0.5)
    axs[i].grid(True, which='minor', linestyle=':', linewidth=0.3)
    ax2.legend(loc='upper right')

    if i == 0:
        ax1.set_title("TVWS RSSI and Soil Temperature Over Time")

fig.tight_layout()
plt.show()

