from Codebase.Generic_VENV_Manger.venv_util import VENVUtil
from Codebase.Pathing.get_analysis_folder import get_analysis_folder
from Codebase.Pathing.get_project_root import get_project_root


def run() -> None:
    analysis_folder = get_analysis_folder()

    analysis_to_run = analysis_folder / "demo_analysis1.py"
    VENVUtil.run_with_venv(str(get_project_root()), str(analysis_to_run))

if __name__ == "__main__":
    run()