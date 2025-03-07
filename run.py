from Codebase.Generic_VENV_Manger.venv_util import VENVUtil
from Codebase.Pathing.get_analysis_folder import get_analysis_folder
from Codebase.Pathing.get_project_root import get_project_root


def run() -> None:
    analysis_folder = get_analysis_folder()
    '''
    #analysis_to_run = analysis_folder / "packet_rate_analyzer.py"
    analysis_to_run = analysis_folder / "urssi_vs_moisture.py"
    #analysis_to_run = analysis_folder / "drssi_vs_moisture.py"


    VENVUtil.run_with_venv(str(get_project_root()), str(analysis_to_run))

    #data_loader = get_project_root() / "Codebase" / "DataLoader" / "data_loader.py"
    #VENVUtil.run_with_venv(str(get_project_root()), str(data_loader))
    '''
    scripts = {
        "1": ("packet_rate_analyzer.py", []),
        "2": ("urssi_vs_moisture.py", ["tvws_instance", "soil_moisture_instance"]),
        "3": ("drssi_vs_moisture.py", ["tvws_instance", "soil_moisture_instance"]),
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
        inputs[param] = get_int_input(f"Enter {param}: ")

    print(f"Running: {analysis_folder / analysis_to_run} with parameters {inputs}")


    # Call method to execute the script (e.g., using subprocess or importing and running the function)

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

if __name__ == "__main__":
    run()