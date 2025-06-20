#!/bin/bash

# Get the root of the project (where setup_linux.sh lives)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT

# Add Codebase to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/Codebase:$PYTHONPATH"


# Install Python
bash "$PROJECT_ROOT/Codebase/Setup/install_python.sh"

# Run setup_files.py
echo "[INFO] Running setup_files.py..."
python3 "$PROJECT_ROOT/Codebase/Setup/setup_files.py"

# Create VENV and install requirements
bash "$PROJECT_ROOT/Codebase/Setup/setup_venv.sh" -venv "$EXISTING_VENV"

echo "----------------------------------------------------"
echo "Setup complete."
echo "Then run './run.sh' to begin."
