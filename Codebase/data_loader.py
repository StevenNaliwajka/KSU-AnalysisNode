import os
import pandas as pd
import re

class DataLoader:
    def __init__(self, base_path="KSU-AnalysisNode/Data"):
        self.base_path = base_path
        self.data = {"SoilData": [], "TVWSScenario": []}
        self.load_all_data()

    def load_all_data(self):
        """Recursively loads all CSV files into categorized dictionaries."""
        for root, _, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(".csv"):
                    full_path = os.path.join(root, file)
                    if file.startswith("SoilData"):
                        self.data["SoilData"].append((file, full_path))
                    elif file.startswith("TVWSScenario"):
                        self.data["TVWSScenario"].append((file, full_path))

    def get_data(self, data_type, filter_key=None):
        """
        Retrieves DataFrames of a specific type.

        Parameters:
        - data_type: "SoilData" or "TVWSScenario"
        - filter_key: A specific filter (e.g., "radio2" for TVWSScenario)

        Returns:
        - A dictionary of filenames mapped to their DataFrame.
        """
        if data_type not in self.data:
            raise ValueError("Invalid data type. Use 'SoilData' or 'TVWSScenario'.")

        filtered_files = []
        if filter_key:
            regex = re.compile(rf"{filter_key}.*\.csv", re.IGNORECASE)
            filtered_files = [(f, p) for f, p in self.data[data_type] if regex.search(f)]
        else:
            filtered_files = self.data[data_type]

        result = {f: pd.read_csv(p) for f, p in filtered_files}
        return result


# Example Usage:
if __name__ == "__main__":
    loader = DataLoader()

    # Get all TVWSScenario radio2 files across all date folders
    radio2_data = loader.get_data("TVWSScenario", "radio2")

    # Display first few rows of each file
    for filename, df in radio2_data.items():
        print(f"File: {filename}\n{df.head()}\n")
