import os
import pandas as pd
import re

from Codebase.Pathing.get_data_folder import get_data_folder
from Codebase.Pathing.get_project_root import get_project_root

class DataLoader:
    def __init__(self):
        self.project_root = get_project_root()
        self.data_folder = get_data_folder()
        self.data = {}

    def load_data(self, csv_category: str, instance_id: int, set_of_columns: set) -> None:
        all_folders = self.get_date_folders()

        for folder in all_folders:
            print(f"[DEBUG] Scanning folder: {folder}")
            for file in os.listdir(folder):
                if not file.endswith(".csv"):
                    continue

                print(f"[DEBUG] Found file: {file}")

                if not self._matches_file(file, csv_category, instance_id):
                    continue

                print(f"[DEBUG] Matched: {file} for category '{csv_category}', instance '{instance_id}'")

                full_path = os.path.join(folder, file)

                try:
                    skip_rows = 0 if instance_id == 0 else 2  # AmbientWeather starts at row 0, others skip metadata
                    data_df = pd.read_csv(full_path, skiprows=skip_rows, low_memory=False)

                    # Normalize columns
                    data_df.columns = [col.strip().lower() for col in data_df.columns]
                    requested_columns = {col.strip().lower() for col in set_of_columns}
                    matching_columns = [col for col in data_df.columns if col in requested_columns]

                    if not matching_columns:
                        print(f"[WARN] Skipping {file}: None of the requested columns found.")
                        continue

                    data_df = data_df[matching_columns]

                    if csv_category not in self.data:
                        self.data[csv_category] = {}

                    key = f"{csv_category}_instance{instance_id}"
                    if key not in self.data[csv_category]:
                        self.data[csv_category][key] = {"data": []}

                    self.data[csv_category][key]["data"].append(data_df)

                    print(f"[INFO] Loaded: {file} | Columns: {list(data_df.columns)}")

                except Exception as e:
                    print(f"[ERROR] Skipping {file} due to error: {e}")

    def load_metadata(self, csv_category: str, instance_id: int) -> dict:
        all_folders = self.get_date_folders()
        metadata_list = []

        for folder in all_folders:
            for file in os.listdir(folder):
                if not file.endswith(".csv"):
                    continue
                if not self._matches_file(file, csv_category, instance_id):
                    continue

                full_path = os.path.join(folder, file)

                try:
                    metadata = self._extract_metadata(full_path)
                    if metadata:
                        metadata_list.append(metadata)
                        print(f"[INFO] Loaded Metadata: {file} | Keys: {list(metadata.keys())}")
                except Exception as e:
                    print(f"[ERROR] Skipping metadata for {file}: {e}")

        return metadata_list

    def get_date_folders(self):
        return [
            os.path.join(self.data_folder, folder)
            for folder in os.listdir(self.data_folder)
            if os.path.isdir(os.path.join(self.data_folder, folder))
        ]

    def _matches_file(self, file_name: str, category: str, instance_id: int) -> bool:
        if instance_id == 0 and category.lower() == "ambientweather":
            return file_name.lower().startswith("ambient-weather-") and file_name.endswith(".csv")
        pattern = rf"^{category}_instance{instance_id}.*\.csv$"
        return bool(re.match(pattern, file_name))

    def _extract_metadata(self, file_path: str) -> dict:
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
    loader.load_data("TVWSScenario", 2, {"US1", "US0", "URSSI"})
    loader.load_data("SoilData", 2, {"Soil Moisture Value", "Soil Moisture (%)"})
    loader.load_data("AmbientWeather", 0, {"date", "simple date", "humidity (%)"})
    print(loader.data)
