from Codebase.Generic_VENV_Manger.venv_util import VENVUtil
from Codebase.Pathing.get_project_root import get_project_root


def setup() -> None:
    VENVUtil.setup_venv(str(get_project_root()))


if __name__ == '__main__':
    setup()