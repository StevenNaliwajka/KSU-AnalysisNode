import os


def ensure_venv_path(venv_destination_folder):
    """Ensure the venv path ends with the correct '/venv' or '\\venv' based on OS."""
    venv_folder_name = "venv"

    # Normalize the path
    venv_destination_folder = os.path.normpath(venv_destination_folder)

    # Check if the path already ends with 'venv'
    if not venv_destination_folder.endswith(os.path.sep + venv_folder_name):
        venv_destination_folder = os.path.join(venv_destination_folder, venv_folder_name)

    return venv_destination_folder

