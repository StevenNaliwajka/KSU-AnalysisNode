from generic_file_io.core.generic_create_folder import generic_create_folder

from Codebase.Pathing.get_data_folder import get_data_folder
from Codebase.Pathing.get_raw_data import get_raw_data
from Codebase.Pathing.get_raw_photos import get_raw_photos


def setup_files():
    # Create raw photos
    generic_create_folder(get_raw_photos())

    # Create raw data
    generic_create_folder(get_raw_data())

    # Create Data folder
    generic_create_folder(get_data_folder())

if __name__ == '__main__':
    setup_files()
