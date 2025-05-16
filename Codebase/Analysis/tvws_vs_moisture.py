import subprocess
from datetime import datetime


from Pathing.get_graph_comp import get_graph_comp
from Pathing.get_graph_folder import get_graph_folder
from Pathing.get_output import get_output
from Pathing.get_project_root import get_project_root
from generic_file_io.core.generic_create_folder import generic_create_folder


def tvws_vs_moisture():
    graph_scripts = {
        "normalized_scatter": "pt_vs_pt_normalized_scatter.py"
    }
    soil_values = {
        "soil_moisture": "Soil Moisture Value",
        "soil_temperature": "Soil Temperature (°C)"
    }
    tvws_values = {
        "drssi": "DRSSI",
        "urssi": "URSSI",
        "dsnr": "DSNR",
        "usnr": "USNR",
    }

    # Create date folder
    date = datetime.today().strftime('%Y-%m-%d')
    output_folder = get_output() / date
    generic_create_folder(output_folder)

    graph_comp_path = get_graph_comp() / "four_x_four_analysis.py"

    for graph_script in graph_scripts:
        # Create analysis folder
        analysis_folder = output_folder / graph_script
        generic_create_folder(analysis_folder)

        graph_script_path = get_graph_folder() / graph_scripts[graph_script]

        for soil_value in soil_values:
            # Create soil folder
            soil_folder = analysis_folder / soil_value
            generic_create_folder(soil_folder)

            for tvws_value in tvws_values:
                # Create TVWS folder
                tvws_folder = soil_folder / tvws_value
                generic_create_folder(tvws_folder)

                final_file_name = f"graph_4x4_{graph_script}_{soil_value}_{tvws_value}.png"
                final_file_path = tvws_folder / final_file_name

                subprocess.run([
                    "python3",
                    str(graph_comp_path),
                    str(graph_script_path),
                    str(final_file_path),
                    tvws_value,
                    tvws_values[tvws_value],
                    soil_value,
                    soil_values[soil_value]
                ], check=True)

            # analysis_script:str, output_path:str, comp_1:str, comp_1_id:str, comp_2:str, comp_2_id:str
    '''
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), analysis_script, "drssi", "drssi",
                           "soil_moisture", "Soil Moisture Value")
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), analysis_script, "urssi", "URSSI",
                           "soil_moisture", "Soil Moisture Value")
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), analysis_script, "dsnr", "DSNR",
                           "soil_moisture", "Soil Moisture Value")
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), analysis_script, "usnr", "USNR",
                           "soil_moisture", "Soil Moisture Value")

    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), analysis_script, "drssi", "drssi",
                           "soil_temp", "Soil Temperature (°C)")
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), analysis_script, "urssi", "URSSI",
                           "soil_temp", "Soil Temperature (°C)")
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), analysis_script, "dsnr", "DSNR",
                           "soil_temp", "Soil Temperature (°C)")
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), analysis_script, "usnr", "USNR",
                           "soil_temp", "Soil Temperature (°C)")
    '''

if __name__ == "__main__":
    tvws_vs_moisture()