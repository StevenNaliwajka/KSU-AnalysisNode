'''
# Not sure why it fails in other places but works here without this import... more research to be done.
import sys
from pathlib import Path

# Dynamically find the project root, required to allow for correct imports.
folder_ct = 2  ### NOT always 2. Change to the qty of folders up before root.
PROJECT_ROOT = Path(__file__).resolve().parents[folder_ct]
sys.path.append(str(PROJECT_ROOT))
'''
import os
import pandas as pd
import re

from Codebase.Pathing.get_data_folder import get_data_folder
from Codebase.Pathing.get_project_root import get_project_root

class DataLoader:
    def __init__(self):
        self.project_root = get_project_root()
        self.data_folder = get_data_folder()
        self.data = {}  # Dictionary to store data dynamically

    def load_data(self, csv_category: str, instance_id: int, set_of_columns: set) -> None:
        """
        Loads regular data (excluding metadata) for a specific category and instance ID across all date folders.
        Assumes the actual data table starts at line 3 (index 2).

        Parameters:
        - csv_category: The general category of data (e.g., "SoilData", "TVWSScenario", "NewCategory").
        - instance_id: The number in the filename (e.g., 1 for SoilData-1, radio1, etc.).
        - set_of_columns: A set of column names to load.

        Returns:
        - None (stores results in self.data)
        """
        all_folders = self.get_date_folders()
        data_frames = []

        for folder in all_folders:
            for file in os.listdir(folder):
                if file.endswith(".csv") and self._matches_file(file, csv_category, instance_id):
                    full_path = os.path.join(folder, file)

                    try:
                        # Skip top two lines due to headder
                        data_df = pd.read_csv(full_path, skiprows=2, low_memory=False)

                        # Normalize column names
                        data_df.columns = [col.strip().lower() for col in data_df.columns]

                        # Normalize requested column
                        requested_columns = {col.strip().lower() for col in set_of_columns}

                        # Find matching columns
                        matching_columns = [col for col in data_df.columns if col in requested_columns]

                        if not matching_columns:
                            print(f"Skipping {file}: None of the requested columns found in regular data.")
                            # print(f"Available columns: {list(data_df.columns)}")
                            continue

                        # Filter data to requested columns
                        data_df = data_df[matching_columns]

                        # Store data dynamically
                        if csv_category not in self.data:
                            self.data[csv_category] = {}

                        key = f"{csv_category}_instance{instance_id}"
                        if key not in self.data[csv_category]:
                            self.data[csv_category][key] = {"data": []}

                        self.data[csv_category][key]["data"].append(data_df)

                        print(f"Loaded: {file} | Columns: {matching_columns}")

                    except Exception as e:
                        print(f"Skipping {file}: {e}")

    def load_metadata(self, csv_category: str, instance_id: int) -> dict:
        """
        Loads metadata for a specific category and instance ID across all date folders.
        Assumes metadata is in the first two lines of the CSV.

        Parameters:
        - csv_category: The general category of data (e.g., "SoilData", "TVWSScenario", "NewCategory").
        - instance_id: The number in the filename (e.g., 1 for SoilData-1, radio1, etc.).

        Returns:
        - A dictionary containing metadata
        """
        all_folders = self.get_date_folders()
        metadata_list = []

        for folder in all_folders:
            for file in os.listdir(folder):
                if file.endswith(".csv") and self._matches_file(file, csv_category, instance_id):
                    full_path = os.path.join(folder, file)

                    try:
                        # Read only the first two lines of metadata
                        metadata = self._extract_metadata(full_path)
                        if metadata:
                            metadata_list.append(metadata)
                            print(f"Loaded Metadata: {file} | Keys: {list(metadata.keys())}")

                    except Exception as e:
                        print(f"Skipping metadata for {file}: {e}")

        return metadata_list

    def get_date_folders(self):
        # Gets date folders
        return [
            os.path.join(self.data_folder, folder)
            for folder in os.listdir(self.data_folder)
            if os.path.isdir(os.path.join(self.data_folder, folder))
        ]

    def _matches_file(self, file_name: str, category: str, instance_id: int) -> bool:
        # checks if any file in the date folder matches the correct instance orientation
        pattern = rf"^{category}_instance{instance_id}.*\.csv$"
        return bool(re.match(pattern, file_name))

    def _extract_metadata(self, file_path: str) -> dict:
        # pulls out the metadata dict. Returns it as a dict.... tbd if thats best
        metadata = {}
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines[:2]:
            key_value = line.strip().split(",")
            if len(key_value) == 2:
                metadata[key_value[0].strip()] = key_value[1].strip()

        return metadata if metadata else None

# EX:
if __name__ == "__main__":
    loader = DataLoader()

    # Load "radio2" files dynamically (no hardcoding)
    loader.load_data("TVWSScenario", 2, {"US1", "US0", "URSSI"})

    # Load "SoilData-1" dynamically
    loader.load_data("SoilData", 1, {"Soil Moisture Value", "Soil Moisture (%)"})


    # Load a hypothetical new dataset category: "NewCategory_instance5"
    # loader.load_data("NewCategory", 5, {"FieldA", "FieldB"})

    # Check stored data dynamically
    print(loader.data)