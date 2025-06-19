from Codebase.Pathing.get_data_folder import get_data_folder
from Codebase.Pathing.get_raw_data import get_raw_data
from Codebase.Pathing.get_raw_photos import get_raw_photos


def setup_files():
    # Create folders
    raw_photos_path = get_raw_photos()
    raw_photos_path.mkdir(parents=True, exist_ok=True)

    raw_data_path = get_raw_data()
    raw_data_path.mkdir(parents=True, exist_ok=True)

    data_path = get_data_folder()
    data_path.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    setup_files()
