import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from unicodedata import category

from Codebase.DataLoader.data_loader import DataLoader


def packet_rate_analyzer(instance_id: int):
    loader = DataLoader()
    category = "TVWSScenario"
    loader.load_data(category, instance_id, {"UTxPackets (Pkts.)", "URxPackets (Pkts.)"})  # Using correct column names
    radio_key = f"{category}_instance{instance_id}"

    if category not in loader.data or radio_key not in loader.data[category]:
        print(f"No data found for {radio_key}")
        return

    for df in loader.data[category][radio_key]["data"]:
        if df.shape[1] < 2:
            print("Skipping dataset due to insufficient columns.")
            continue

        print("Available columns:", df.columns.tolist())  # Debugging line

        try:
            # Normalize column names by stripping spaces and making lowercase
            df.columns = [col.strip().lower() for col in df.columns]

            # Define expected column names in lowercase
            sent_col = "utxpackets (pkts.)"
            recv_col = "urxpackets (pkts.)"

            if sent_col not in df.columns or recv_col not in df.columns:
                print(f"Skipping dataset: Required columns not found. Available columns: {df.columns.tolist()}")
                continue

            # Extract elapsed time and packet counts
            elapsed_time = np.arange(len(df)) * 5 / 60  # Convert to minutes

            # Convert columns to numeric, handling non-numeric values
            sent_packets = pd.to_numeric(df[sent_col], errors='coerce').fillna(0)
            received_packets = pd.to_numeric(df[recv_col], errors='coerce').fillna(0)

            # Compute packet rate (packets per second)
            data1 = np.diff(sent_packets) / 5
            data2 = np.diff(received_packets) / 5

            # Apply rolling average to smooth data
            window_size = 10  # Adjust window size for smoothing effect
            smoothed_data1 = pd.Series(data1).rolling(window=window_size, min_periods=1).mean()
            smoothed_data2 = pd.Series(data2).rolling(window=window_size, min_periods=1).mean()

            mean1, mean2 = np.mean(data1), np.mean(data2)

            # Handle empty data cases
            if np.isnan(mean1) or np.isnan(mean2):
                print("Warning: No valid data points found after filtering.")
                continue

            # Determine Y-axis limits dynamically
            min_y = max(0, min(np.min(smoothed_data1), np.min(smoothed_data2), 100))
            max_y = max(np.max(smoothed_data1), np.max(smoothed_data2)) + 5

            # Plot data
            plt.figure()
            plt.plot(elapsed_time[:len(smoothed_data1)], smoothed_data1, 'b-', label='Transmitted Packets Per Second')
            plt.plot(elapsed_time[:len(smoothed_data2)], smoothed_data2, 'r-', label='Received Packets Per Second')

            # Add mean lines
            plt.axhline(mean1, color='k', linestyle='--', linewidth=2)
            plt.axhline(mean2, color='k', linestyle='--', linewidth=2)

            # Place mean text in the top-left of the plot
            plt.annotate(f'Mean Sent: {mean1:.2f}', xy=(0.02, 0.95), xycoords='axes fraction', fontsize=12,
                         fontweight='bold', color='b')
            plt.annotate(f'Mean Received: {mean2:.2f}', xy=(0.02, 0.90), xycoords='axes fraction', fontsize=12,
                         fontweight='bold', color='r')

            # Labels and Title
            plt.xlabel('Elapsed Time (Minutes)')
            plt.ylabel('Packets Per Second')
            plt.title(f'{category} - Instance {instance_id}')
            plt.legend()
            plt.ylim([min_y, max_y])
            plt.grid(True)
            plt.show()
        except Exception as e:
            print(f"Error processing data for {radio_key}: {e}")


# Usage Example
if __name__ == "__main__":
    args = sys.argv[1:]

    req_value = 1
    if len(args) < req_value:
        print(f"Error: Not enough arguments provided. Expected {req_value} values.")
        sys.exit(1)
    tvws_instance = int(args[0])

    packet_rate_analyzer(tvws_instance)