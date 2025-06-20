# run_dashboard.py

import os
import sys

# Add Codebase to PYTHONPATH (in case it's not already)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, os.path.join(project_root, "Codebase"))

# Import and run the dashboard
from Dashboard.dashboard import main

if __name__ == "__main__":
    main()
