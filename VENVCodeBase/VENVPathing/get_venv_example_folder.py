import os

from ..VENVPathing.get_venv_root import get_venv_root

def get_venv_example_folder() -> str:
    venv_example_folder_name = ["VENVSetup", "VENVExampleJSON"]
    venv_root = get_venv_root()
    folder_path = os.path.join(venv_root, *venv_example_folder_name)
    # print(folder_path)
    return folder_path

if __name__ == '__main__':
    get_venv_example_folder()
