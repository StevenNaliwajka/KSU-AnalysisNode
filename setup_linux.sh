#!/bin/bash

# Get the root of the project (where setup_linux.sh lives)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT

# Ensure Data folder exists
DATA_DIR="$PROJECT_ROOT/Data"
if [ ! -d "$DATA_DIR" ]; then
  echo "[INFO] Creating missing Data directory at $DATA_DIR"
  mkdir -p "$DATA_DIR"
else
  echo "[INFO] Data directory already exists at $DATA_DIR"
fi

# Setup Configs

# Install Python
bash "$PROJECT_ROOT/Codebase/Setup/install_python.sh"

# Create VENV and install requirements
bash "$PROJECT_ROOT/Codebase/Setup/setup_venv.sh" -venv "$EXISTING_VENV"

echo "Configure Configs In /Config/*"
echo "Once finished run './run.sh'"
