import os
import shutil
import pandas as pd

from Codebase.Pathing.get_project_root import get_project_root
from Codebase.Pathing.get_raw_data import get_raw_data


def process_csv(file_path: str, output_path: str, filter_columns: list):
    # Read the first two lines (metadata)
    with open(file_path, "r") as f:
        metadata = [next(f) for _ in range(2)]

    # Read the CSV while skipping the first two rows for processing
    df = pd.read_csv(file_path, skiprows=2)

    # Ensure the specified filter columns exist before filtering
    for filter_column in filter_columns:
        if filter_column in df.columns:
            df = df[df[filter_column] != 0]
        else:
            print(f"Warning: '{filter_column}' column not found in {file_path}")

    # Save the metadata and cleaned data to a new CSV file
    with open(output_path, "w") as f:
        f.writelines(metadata)
    df.to_csv(output_path, mode="a", index=False, header=True)


def data_cleaner(root_dir: str):
    data_in_path = str(get_raw_data())
    data_out_path = os.path.join(root_dir, "Data")

    # Define sections to scan and their corresponding filter columns
    sections = {
        "TVWSScenario": ["DRSSI", "URSSI"],
        "SoilData": ["Soil Moisture Value"]
    }

    for date_folder in os.listdir(data_in_path):
        date_folder_path = os.path.join(data_in_path, date_folder)
        if not os.path.isdir(date_folder_path):
            continue

        output_date_folder = os.path.join(data_out_path, date_folder)
        os.makedirs(output_date_folder, exist_ok=True)

        for file_name in os.listdir(date_folder_path):
            file_path = os.path.join(date_folder_path, file_name)
            if not file_name.endswith(".csv"):
                continue

            # Determine which section the file belongs to
            filter_columns = None
            for section, columns in sections.items():
                if section in file_name:
                    filter_columns = columns
                    break

            if filter_columns:
                output_file_path = os.path.join(output_date_folder, file_name)
                process_csv(file_path, output_file_path, filter_columns)
                os.remove(file_path)  # Delete original file after processing

        # Remove the empty date folder
        if not os.listdir(date_folder_path):
            os.rmdir(date_folder_path)


if __name__ == "__main__":
    root_directory = get_project_root()  # Adjust this if needed
    data_cleaner(str(root_directory))