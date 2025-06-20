import os
import sys

from Codebase.Pathing.get_ml_bin_folder import get_ml_bin_folder

# Add project root to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.append(PROJECT_ROOT)

# Now your imports
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
    predict_atm = data_folder/"Predict"/"Atmospheric"
    predict_atm.mkdir(parents=True, exist_ok=True)
    predict_sdr = data_folder/"Predict"/"SDR"
    predict_sdr.mkdir(parents=True, exist_ok=True)
    predict_soil = data_folder/"Predict"/"Soil"
    predict_soil.mkdir(parents=True, exist_ok=True)
    predict_tvws = data_folder/"Predict"/"TVWS"
    predict_tvws.mkdir(parents=True, exist_ok=True)
    train_atm = data_folder/"Train"/"Atmospheric"
    train_atm.mkdir(parents=True, exist_ok=True)
    train_sdr = data_folder/"Train"/"SDR"
    train_sdr.mkdir(parents=True, exist_ok=True)
    train_soil = data_folder/"Train"/"Soil"
    train_soil.mkdir(parents=True, exist_ok=True)
    train_tvws = data_folder/"Train"/"TVWS"
    train_tvws.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    setup_files()
