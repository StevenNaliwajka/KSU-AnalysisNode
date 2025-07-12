import os
import sys

# Add project root to path BEFORE any Codebase import
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now safe to import project files
from Codebase.Pathing.get_ml_bin_folder import get_ml_bin_folder
from Codebase.Pathing.get_data_folder import get_data_folder
from Codebase.Pathing.get_raw_photos import get_raw_photos


def setup_files():
    # Create folders
    raw_photos_path = get_raw_photos()
    raw_photos_path.mkdir(parents=True, exist_ok=True)

    data_path = get_data_folder()
    data_path.mkdir(parents=True, exist_ok=True)

    ml_bin_folder = get_ml_bin_folder()
    ml_bin_folder.mkdir(parents=True, exist_ok=True)

    # Create Data folder paths
    data_folder = data_path
    (data_folder / "Predict" / "Ambient").mkdir(parents=True, exist_ok=True)
    (data_folder / "Predict" / "SDR").mkdir(parents=True, exist_ok=True)
    (data_folder / "Predict" / "Soil").mkdir(parents=True, exist_ok=True)
    (data_folder / "Predict" / "TVWS").mkdir(parents=True, exist_ok=True)
    (data_folder / "Train" / "Ambient").mkdir(parents=True, exist_ok=True)
    (data_folder / "Train" / "SDR").mkdir(parents=True, exist_ok=True)
    (data_folder / "Train" / "Soil").mkdir(parents=True, exist_ok=True)
    (data_folder / "Train" / "TVWS").mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    setup_files()
