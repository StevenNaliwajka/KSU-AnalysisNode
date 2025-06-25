import os
from pathlib import Path

import pandas as pd
import re

from Codebase.DataManager.Processing.FileIO.get_all_csv_files import get_all_csv_files
from Codebase.DataManager.Processing.Header.detect_header_row import detect_header_row
from Codebase.DataManager.Processing.Header.normalize_header import normalize_header
from Codebase.Pathing.get_data_folder import get_data_folder
from Codebase.Pathing.get_project_root import get_project_root
from Codebase.DataManager.Processing.DataMGMT.parse_datetime_column import parse_datetime_column
from Codebase.DataManager.Processing.DataMGMT.scan_available_columns_by_type import scan_available_columns_by_type

class DataLoader:
    def __init__(self, dropdown_blacklist=None):
        self.project_root = get_project_root()
        self.data_folder = get_data_folder()

        # Dictionary used to track which types of data have been found in the data folder.
        # This is populated by scan_available_data_types() and stores a set of type names (e.g., "tvws", "soil", etc.).
        # These are detected based on filename prefixes during recursive folder scanning.
        self.data_types_available = set()

        # Scan the data folder recursively to detect the first occurrence of each known data type.
        # Recognized types include: "tvws", "soil", "ambient", "sdr".
        # Adds each detected type (as a string) to self.data_types_available.
        self.scan_available_data_types()

        # A dictionary mapping each data type (e.g., "tvws", "soil") to a list of available column names
        # extracted from the first valid CSV file found in each corresponding subfolder under /Data.
        # Columns listed in the provided blacklist will be excluded from the results.
        # Format:
        # {
        #     "tvws": ["drssi", "frequency", ...],
        #     "soil": ["soil moisture value", "soil temp (c)", ...],
        #     ...
        # }
        self.column_list_by_type = scan_available_columns_by_type(dropdown_blacklist)
        # print(self.column_list_by_type)

        self.all_csv_files = get_all_csv_files()

        self.data = {}
        """
        Structure of `self.data`

        After calling `load_data(csv_category, instance_id, set_of_columns)`, the `self.data` dictionary
        is populated with time-aligned data for each CSV category and instance.

        self.data structure:
        {
            "<csv_category>": {
                "file_name": {
                    "data": [
                        pd.DataFrame with columns:
                            - "datetime" (pd.Timestamp)
                            - <requested column 1>
                            - <requested column 2>
                            - ...
                    ]
                },
                ...
            },
            ...
        }
        
        or 
        
        self.data = {
            "tvws": {
                "tvws_instance0": {
                    "dirt": {
                        "data": [df1, df2, ...]
                    },
                    "gravel": {
                        "data": [df3, ...]
                    },
                }
            },
            "soil": {
                "soil_instance1": {
                    "-1": {
                        "data": [df4, ...]
                    },
                    "-3": {
                        "data": [df5, ...]
                    },
                }
            }
        }


        Key Features:
        - Each DataFrame in the `"data"` list contains **only rows and columns from a single CSV file**.
        - The `"datetime"` column is parsed using custom rules from `datetime_parser.parse_datetime_column()`.
        - All columns are **index-aligned**, meaning the `datetime` and value columns share the same row index.
        - Multiple files for the same category and instance are appended to the `"data"` list.
        - Column names are stored in lowercase to ensure consistency.

        Example:
        self.data["TVWS"]["TVWS_instance1"]["data"][0].head() →

                datetime              drssi
        0   2025-06-06 11:00:00      -91.23
        1   2025-06-06 11:00:05      -90.87
        ...

        Usage Tips:
        - Iterate through all loaded DataFrames like:
            for df in self.data["Soil"]["Soil_instance0"]["data"]:
                # process df

        - Combine all DataFrames for a category-instance:
            all_data = pd.concat(self.data["TVWS"]["TVWS_instance1"]["data"], ignore_index=True)
        """

    @classmethod
    def from_cached_state(cls, dropdown_blacklist, data_types_available, column_list_by_type, all_csv_files):
        """
        Reconstruct a DataLoader object from cached serialized values.
        Used when loading from a Dash dcc.Store or similar.
        """
        obj = cls.__new__(cls)  # Create an uninitialized instance
        obj.project_root = get_project_root()
        obj.data_folder = get_data_folder()

        obj.data_types_available = set(data_types_available)
        obj.column_list_by_type = column_list_by_type
        obj.all_csv_files = [Path(p) for p in all_csv_files]
        obj.blacklist = dropdown_blacklist
        obj.data = {}

        return obj

    def scan_available_data_types(self):
        """
        Recursively scan self.data_folder and collect the first occurrence of each known data type
        (by filename prefix). Updates self.data_types_available as a set: {"tvws", "ambient", ...}
        """
        known_types = {"tvws", "soil", "ambient", "sdr"}
        self.data_types_available = set()

        for root, _, files in os.walk(self.data_folder):
            for file in sorted(files):  # consistent order
                if not file.lower().endswith(".csv"):
                    continue

                name = file.lower()
                for dtype in known_types:
                    if dtype not in self.data_types_available and name.startswith(dtype):
                        self.data_types_available.add(dtype)
                        # print(f"[INFO] Found type: {dtype}")
                        if self.data_types_available == known_types:
                            return  # all types found, stop early

    def load_data(self, csv_category: str, instance_id: int, set_of_columns: set) -> None:
        csv_category = csv_category.lower()
        all_csv_files = self.all_csv_files

        for full_path in all_csv_files:
            file = full_path.name
            # print(f"[DEBUG] Found file: {file}")

            if not self._matches_file(file, csv_category, instance_id):
                # print("file does not match")
                continue


            # print(f"[DEBUG] Matched: {file} for category '{csv_category}', instance '{instance_id}'")

            try:
                # Detect header line
                header_row_index, _ = detect_header_row(str(full_path))
                # print(f"[DEBUG] Detected header row at line {header_row_index} in {file}")

                # Read CSV starting after header
                df = pd.read_csv(full_path, skiprows=header_row_index, header=0, low_memory=False)
                df.columns = [normalize_header(col) for col in df.columns]

                # print(f"[DEBUG] Cleaned column names: {df.columns.tolist()}")

                # Parse datetime
                datetime_series = parse_datetime_column(str(full_path), df)
                if datetime_series.isna().all():
                    print(f"[WARN] No valid datetime found in {file}. Skipping.")
                    continue

                # Match requested columns
                requested = {normalize_header(col) for col in set_of_columns}

                matching = [col for col in df.columns if col in requested]
                if not matching:
                    print(f"[WARN] Skipping {file}: No requested columns found.")
                    continue

                # 🔍 Determine special subkey (TVWS → SpecialValue, Soil → Depth)
                special_key = "unknown"
                if csv_category == "tvws":
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            headers = next(f).strip().split(",")
                            values = next(f).strip().split(",")
                            if "specialvalue" in [h.lower() for h in headers]:
                                idx = [h.lower() for h in headers].index("specialvalue")
                                special_key = values[idx].strip()
                    except Exception as e:
                        print(f"[WARN] Failed to extract SpecialValue from {file}: {e}")

                elif csv_category == "soil":
                    print(f"[DEBUG] Soil columns: {df.columns}")
                    if "depth" in df.columns:
                        depth_vals = df["depth"].dropna().unique()
                        print(f"[DEBUG] Found depths: {depth_vals}")
                        if len(depth_vals) == 1:
                            special_key = normalize_header(str(depth_vals[0]))
                        elif len(depth_vals) > 1:
                            special_key = "mixed-depth"

                # 📦 Construct final DataFrame
                final_df = pd.concat([datetime_series.rename("datetime"), df[matching]], axis=1)

                # 🗂 Set correct storage key
                if csv_category in {"ambientweather", "atmospheric"}:
                    key = csv_category  # no instance
                else:
                    key = f"{csv_category}_instance{instance_id}"

                self.data.setdefault(csv_category, {})
                self.data[csv_category].setdefault(key, {})
                self.data[csv_category][key].setdefault(special_key, {"data": []})
                self.data[csv_category][key][special_key]["data"].append(final_df)

                '''
                print(f"[DEBUG] Attempting to store data:")
                print(f"  - Category: {csv_category}")
                print(f"  - Key: {key}")
                print(f"  - Special Key: {special_key}")
                print(f"  - Columns: {final_df.columns.tolist()}")
                print(f"  - Num rows: {len(final_df)}")
                
                '''

                # print(f"[INFO] Loaded: {file} | Subkey: {special_key} | Columns: {list(final_df.columns)}")

            except Exception as e:
                print(f"[ERROR] Skipping {file} due to error: {e}")

    def load_metadata(self, csv_category: str, instance_id: int) -> list:
        all_csv_files = self.all_csv_files
        metadata_list = []

        for full_path in all_csv_files:
            file = os.path.basename(full_path)

            if not self._matches_file(file, csv_category, instance_id):
                continue

            try:
                metadata = self._extract_metadata(full_path)
                if metadata:
                    metadata_list.append(metadata)
                    # print(f"[INFO] Loaded Metadata: {file} | Keys: {list(metadata.keys())}")
            except Exception as e:
                print(f"[ERROR] Skipping metadata for {file}: {e}")

        return metadata_list

    def _matches_file(self, filename: str, category: str, instance_id: int) -> bool:
        filename = filename.lower()
        category = category.lower()

        # Check category match
        if category == "ambient":
            cat_match = "ambient" in filename
            print(f"[DEBUG] Matching ambient file '{filename}': cat_match={cat_match}")
            return cat_match

        cat_match = category in filename

        if instance_id is None:
            print(
                f"[DEBUG] Matching file '{filename}': cat_match={cat_match}, instance_id=None (skipping instance check)")
            return cat_match

        instance_pattern = re.compile(rf"_{re.escape(str(instance_id))}(?:_|\.|-)?")
        instance_match = bool(instance_pattern.search(filename))

        print(f"[DEBUG] Matching file '{filename}': cat_match={cat_match}, instance_match={instance_match}")
        return cat_match and instance_match

    def _extract_metadata(self, file_path: str) -> dict:
        metadata = {}
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines[:2]:
            key_value = line.strip().split(",")
            if len(key_value) == 2:
                metadata[key_value[0].strip()] = key_value[1].strip()

        return metadata if metadata else None


if __name__ == "__main__":
    print("📂 Scanning data folder:", get_data_folder())

    # Define blacklist — for demo, you can leave it empty or add some known columns
    dropdown_blacklist = {"datetime", "date", "time"}

    # Create loader instance
    loader = DataLoader(dropdown_blacklist)

    print("\n✅ Data Types Detected:")
    for dtype in sorted(loader.data_types_available):
        print(f"  - {dtype}")

    print("\n🧠 Available Columns by Type:")
    for dtype, columns in loader.column_list_by_type.items():
        print(f"  [{dtype}] → {columns}")

    print("\n📄 All CSV Files Found:")
    for path in loader.all_csv_files:
        print(f"  - {path}")
