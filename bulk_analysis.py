from Codebase.Generic_VENV_Manger.venv_util import VENVUtil
from Codebase.Pathing.get_codebase_folder import get_codebase_folder
from Codebase.Pathing.get_project_root import get_project_root


def bulk_analysis():
    # get 4x4 path
    auto_file = get_codebase_folder()/ "AnalysisScripts" / "AutoAnalysis" / "four_x_four_analysis.py"


    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), "rssi", "moisture", "drssi")
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), "rssi", "moisture", "urssi")
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), "snr", "moisture", "dsnr")
    VENVUtil.run_with_venv(str(get_project_root()), str(auto_file), "snr", "moisture", "usnr")

if __name__ == "__main__":
    bulk_analysis()