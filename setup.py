from Codebase.Pathing.get_project_root import get_project_root
from Codebase.Pathing.get_setup_file import get_setup_files_file


def setup() -> None:
    VENVUtil.setup_venv(str(get_project_root()))
    VENVUtil.run_with_venv(str(get_project_root()), str(get_setup_files_file()))


if __name__ == '__main__':
    setup()