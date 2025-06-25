from Codebase.Pathing.get_project_root import get_project_root


def get_dashboard_assets_folder():
    root = get_project_root()
    dashboard_assets_folder = root/"Codebase"/"Dashboard"/"assets"
    return dashboard_assets_folder