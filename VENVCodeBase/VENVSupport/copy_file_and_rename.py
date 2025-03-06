import shutil

def copy_file_and_rename(current_file_path, new_file_path):
    """Copies a file and renames it."""
    try:
        shutil.copy(current_file_path, new_file_path)
        print(f"Successfully copied and renamed the file to {new_file_path}")
    except FileNotFoundError:
        print(f"Error: {current_file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")