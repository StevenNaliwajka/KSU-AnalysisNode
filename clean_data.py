from Codebase.Generic_VENV_Manger.venv_util import VENVUtil
from Codebase.Pathing.get_codebase_folder import get_codebase_folder
from Codebase.Pathing.get_project_root import get_project_root


def clean_data():
    codebase = get_codebase_folder()
    file = codebase / "data_cleaner.py"

    VENVUtil.run_with_venv(str(get_project_root()), file)


if __name__ == "__main__":
    clean_data()