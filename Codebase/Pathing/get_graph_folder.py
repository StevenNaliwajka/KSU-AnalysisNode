from Codebase.Pathing.get_analysis_folder import get_analysis_folder


def get_graph_folder():
    root = get_analysis_folder()
    folder = root / "Graph"
    return folder