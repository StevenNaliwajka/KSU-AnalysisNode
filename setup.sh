#!/bin/bash

# Get the root of the project (where setup.sh lives)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT

# Setup Configs

# Install Python
bash "$PROJECT_ROOT/Codebase/Setup/install_python.sh"

# Create VENV and install requirements
bash "$PROJECT_ROOT/Codebase/Setup/setup_venv.sh" -venv "$EXISTING_VENV"

echo "Configure Configs In /Config/*"
echo "Once finished run './run.sh'"
