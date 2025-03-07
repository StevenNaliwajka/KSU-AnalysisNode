from Codebase.Generic_VENV_Manger.venv_util import VENVUtil
from Codebase.Pathing.get_analysis_folder import get_analysis_folder
from Codebase.Pathing.get_project_root import get_project_root


def run() -> None:
    file = get_analysis_folder() / "tvws_vs_moisture.py"
    VENVUtil.run_with_venv(str(get_project_root()), str(file))


if __name__ == "__main__":
    run()
