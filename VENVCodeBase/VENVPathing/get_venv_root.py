import os


def get_venv_root() -> str:
    # Qty of directories to rise
    num_directories = 3

    # Build path.
    current_directory = os.path.abspath(__file__)
    up_levels = ['..'] * num_directories
    folder_path = os.path.abspath(os.path.join(current_directory, *up_levels))
    # print(folder_path)
    return folder_path

if __name__ == '__main__':
    get_venv_root()
