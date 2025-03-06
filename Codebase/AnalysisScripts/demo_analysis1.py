import sys
from pathlib import Path

# Dynamically find the project root, required to allow for correct imports.
folder_ct = 2  ### NOT always 2. Change to the qty of folders up before root.
PROJECT_ROOT = Path(__file__).resolve().parents[folder_ct]
sys.path.append(str(PROJECT_ROOT))

