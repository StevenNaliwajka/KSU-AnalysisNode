import os
import subprocess
import sys

from .VENVCodeBase.VENVReadJSON.load_env_vars import load_env_vars
from .VENVCodeBase.VENVReadJSON.parse_packages import parse_packages
from .VENVCodeBase.VENVSupport.ensure_venv_path import ensure_venv_path
from .VENVCodeBase.VENVSupport.get_python_executable import get_python_executable


class VENVUtil:
    @staticmethod
    def setup_venv(venv_destination_folder: str) -> None:
        """
        Sets up a virtual environment, installs packages from a JSON config file, and runs the main script.
        """
        # Get package lists from JSON
        config = parse_packages()
        pip_packages = config.get("pip_packages", [])
        github_packages = config.get("github_packages", [])

        venv_destination_folder = ensure_venv_path(venv_destination_folder)

        # Check if venv exists
        if not os.path.exists(venv_destination_folder):
            print("Creating virtual environment...")
            result = subprocess.run([sys.executable, "-m", "venv", venv_destination_folder], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error creating virtual environment: {result.stderr}")
                sys.exit(1)
            else:
                print("Virtual environment created successfully.")

        venv_python = get_python_executable(venv_destination_folder)

        # Ensure the virtual environment's Python exists
        if not os.path.exists(venv_python):
            print(f"Virtual environment Python not found: {venv_python}")
            sys.exit(1)

        # Update pip
        try:
            subprocess.run([venv_python, "-m", "pip", "--version"], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            print("pip is not installed. Installing pip...")
            subprocess.run([venv_python, "-m", "ensurepip", "--upgrade"], check=True)
            subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            print("pip has been installed and upgraded.")

        # Get list of installed packages
        result = subprocess.run([venv_python, "-m", "pip", "list"], capture_output=True, text=True, check=True)
        installed_packages = {line.split()[0].lower() for line in result.stdout.splitlines()[2:]}

        # Install missing standard packages
        missing_pip_packages = [pkg for pkg in pip_packages if pkg.lower() not in installed_packages]
        if missing_pip_packages:
            print(f"Installing missing pip packages: {missing_pip_packages}")
            subprocess.run([venv_python, "-m", "pip", "install"] + missing_pip_packages, check=True)

        # Install GitHub packages separately
        if github_packages:
            print("Installing GitHub packages...")
            for github_pkg in github_packages:
                subprocess.run([venv_python, "-m", "pip", "install", github_pkg], check=True)

        print("Virtual environment setup complete.")

    @staticmethod
    def run_with_venv(venv_destination_folder: str, python_file_to_run: str) -> None:
        """Activate venv and run the script."""
        load_env_vars()

        venv_destination_folder = ensure_venv_path(venv_destination_folder)

        venv_python = get_python_executable(venv_destination_folder)

        if not os.path.exists(venv_python):
            print("Error: Virtual environment not found. Ensure venv is set up correctly.")
            return

        try:
            subprocess.run([venv_python, python_file_to_run], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")

if __name__ == "__main__":
    # Check if arguments were provided
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        VENVUtil.setup_venv(user_input)
    else:
        print("No input provided.")
