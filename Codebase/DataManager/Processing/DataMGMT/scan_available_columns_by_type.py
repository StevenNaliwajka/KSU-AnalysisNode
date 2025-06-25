import os
from pathlib import Path

from Codebase.DataManager.Processing.Header.detect_header_row import detect_header_row
from Codebase.Pathing.get_data_folder import get_data_folder


def scan_available_columns_by_type(blacklist=None):
    """
    Scan each data type subfolder under the root data folder and return a dictionary
    of available column headers per type, using the first valid CSV file found in each folder.

    Args:
        blacklist (list[str] or set[str], optional): A list of column names to exclude from the results.
                                                    If None, all columns are included.

    Returns:
        dict[str, list[str]]: A dictionary where keys are folder names (data types like "tvws", "soil", etc.)
                              and values are lists of column names (in lowercase, stripped form) found in
                              the first CSV file detected in each subfolder.

    Example return:
        {
            "tvws": ["drssi", "frequency"],
            "soil": ["soil moisture value", "soil temp (c)"],
            ...
        }
    """
    seen_types = set()
    available_columns = {}

    # ✅ Set root to the actual 'Train' directory
    root_data_folder = get_data_folder() / "Train"

    # Normalize blacklist
    blacklist = {x.strip().lower() for x in blacklist} if blacklist else set()

    for path in root_data_folder.rglob("*.csv"):
        parts = path.relative_to(root_data_folder).parts
        if len(parts) < 2:
            continue  # Skip CSVs directly in 'Train'

        data_type = parts[0].lower()  # 'soil', 'tvws', etc.
        if data_type in seen_types:
            continue

        try:
            header_row, columns = detect_header_row(path)
            if columns:
                filtered = [col for col in columns if col.strip().lower() not in blacklist]
                available_columns[data_type] = filtered
                seen_types.add(data_type)
        except Exception as e:
            print(f"[ERROR] Couldn't process {path}: {e}")

    return available_columns