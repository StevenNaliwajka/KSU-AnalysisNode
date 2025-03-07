from Codebase.Pathing.get_analysis_folder import get_analysis_folder
from Codebase.Pathing.get_codebase_folder import get_codebase_folder
from Codebase.Pathing.get_graph_folder import get_graph_folder


def get_graph_comp():
    root = get_analysis_folder()
    folder = root / "GraphComp"
    return folder

if __name__ == "__main__":
    print(get_graph_comp())