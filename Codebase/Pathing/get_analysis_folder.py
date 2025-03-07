from pathlib import Path

from Codebase.Pathing.get_project_root import get_project_root


def get_analysis_folder() -> Path:
    root = get_project_root()
    folder = root / "Codebase" / "Analysis"
    return folder