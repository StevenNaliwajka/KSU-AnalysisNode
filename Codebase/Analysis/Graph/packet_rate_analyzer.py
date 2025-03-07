import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Codebase.DataManager.data_loader import DataLoader


def packet_rate_analyzer(instance_id: int, output_path: str = None):
    loader = DataLoader()
    category = "TVWSScenario"
    loader.load_data(category, instance_id, {"UTxPackets (Pkts.)", "URxPackets (Pkts.)"})
    radio_key = f"{category}_instance{instance_id}"

    if category not in loader.data or radio_key not in loader.data[category]:
        print(f"No data found for {radio_key}")
        return

    for df in loader.data[category][radio_key]["data"]:
        if df.shape[1] < 2:
            print("Skipping dataset due to insufficient columns.")
            continue

        # print("Available columns:", df.columns.tolist())

        try:
            df.columns = [col.strip().lower() for col in df.columns]
            sent_col = "utxpackets (pkts.)"
            recv_col = "urxpackets (pkts.)"

            if sent_col not in df.columns or recv_col not in df.columns:
                print(f"Skipping dataset: Required columns not found. Available columns: {df.columns.tolist()}")
                continue

            elapsed_time = np.arange(len(df)) * 5 / 60
            sent_packets = pd.to_numeric(df[sent_col], errors='coerce').fillna(0)
            received_packets = pd.to_numeric(df[recv_col], errors='coerce').fillna(0)

            data1 = np.diff(sent_packets) / 5
            data2 = np.diff(received_packets) / 5

            window_size = 10
            smoothed_data1 = pd.Series(data1).rolling(window=window_size, min_periods=1).mean()
            smoothed_data2 = pd.Series(data2).rolling(window=window_size, min_periods=1).mean()

            mean1, mean2 = np.mean(data1), np.mean(data2)

            if np.isnan(mean1) or np.isnan(mean2):
                print("Warning: No valid data points found after filtering.")
                continue

            min_y = max(0, min(np.min(smoothed_data1), np.min(smoothed_data2), 100))
            max_y = max(np.max(smoothed_data1), np.max(smoothed_data2)) + 5

            plt.figure()
            plt.plot(elapsed_time[:len(smoothed_data1)], smoothed_data1, 'b-', label='Transmitted Packets Per Second')
            plt.plot(elapsed_time[:len(smoothed_data2)], smoothed_data2, 'r-', label='Received Packets Per Second')

            plt.axhline(mean1, color='k', linestyle='--', linewidth=2)
            plt.axhline(mean2, color='k', linestyle='--', linewidth=2)

            plt.annotate(f'Mean Sent: {mean1:.2f}', xy=(0.02, 0.95), xycoords='axes fraction', fontsize=12,
                         fontweight='bold', color='b')
            plt.annotate(f'Mean Received: {mean2:.2f}', xy=(0.02, 0.90), xycoords='axes fraction', fontsize=12,
                         fontweight='bold', color='r')

            plt.xlabel('Elapsed Time (Minutes)')
            plt.ylabel('Packets Per Second')
            plt.title(f'{category} - Instance {instance_id}')
            plt.legend()
            plt.ylim([min_y, max_y])
            plt.grid(True)

            if output_path:
                plt.savefig(output_path)
                print(f"Graph saved to {output_path}")
            else:
                plt.show()

        except Exception as e:
            print(f"Error processing data for {radio_key}: {e}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        print("Error: Not enough arguments provided. Expected at least 1 value.")
        sys.exit(1)

    tvws_instance = int(args[0])
    output_path = args[1] if len(args) > 1 else None

    packet_rate_analyzer(tvws_instance, output_path)
