from Codebase.Generic_VENV_Manger.venv_util import VENVUtil
from Codebase.Pathing.get_analysis_folder import get_analysis_folder
from Codebase.Pathing.get_project_root import get_project_root


def run() -> None:
    analysis_folder = get_analysis_folder()

    scripts = {
        "1": ("packet_rate_analyzer.py", ["tvws_instance"]),
        "2": ("rssi_vs_moisture.py", ["tvws_instance", "soil_moisture_instance", "\"drssi\" or \"urssi\""]),
        "3": ("snr_vs_moisture.py", ["tvws_instance", "soil_moisture_instance", "\"dsnr\" or \"usnr\""])
    }

    print("Select an analysis script to run:")
    for key, (script, _) in scripts.items():
        print(f"{key}: {script}")

    choice = input("Enter the number of the script to run: ")
    if choice not in scripts:
        print("Invalid choice. Exiting.")
        return

    analysis_to_run, required_inputs = scripts[choice]
    inputs = {}

    for param in required_inputs:
        inputs[param] = get_input(f"Enter {param}: ")

    print(f"Running: {analysis_folder / analysis_to_run} with parameters {inputs}")

    # Convert input arguments to a list of strings
    input_args = [str(value) for value in inputs.values()]

    # Run the selected script with the virtual environment
    VENVUtil.run_with_venv(str(get_project_root()), str(analysis_folder / analysis_to_run), *input_args)


def get_input(prompt):
    while True:
        try:
            return input(prompt)
        except ValueError:
            print("Invalid input.")


if __name__ == "__main__":
    run()
