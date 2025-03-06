import os


def get_python_executable(venv_destination_folder):
    """Get the correct python executable inside the virtual environment."""
    if os.name == "nt":  # Windows
        return os.path.join(venv_destination_folder, "Scripts", "python.exe")
    else:  # macOS/Linux
        return os.path.join(venv_destination_folder, "bin", "python")