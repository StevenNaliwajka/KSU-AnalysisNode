#!/bin/bash
# setup_linux.sh
# Main setup script for the project

# --- Variables ---
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT
export PYTHONPATH="$PROJECT_ROOT/Codebase:$PYTHONPATH"

# --- Install Python ---
bash "$PROJECT_ROOT/Codebase/Setup/install_python.sh"

# --- Run setup_files.py ---
echo "[INFO] Running setup_files.py..."
python3 "$PROJECT_ROOT/Codebase/Setup/setup_files.py"

# --- Create virtual environment & install requirements ---
bash "$PROJECT_ROOT/Codebase/Setup/setup_venv.sh" -venv "$EXISTING_VENV"

# --- Configure hosting (IP, port, NAS, reboot schedule) ---
echo "[INFO] Configuring hosting..."
bash "$PROJECT_ROOT/Codebase/Setup/configure_hosting_linux.sh"

# --- Configure systemd services (NAS, Dashboard, Reboot) ---
echo "[INFO] Configuring systemd services..."
bash "$PROJECT_ROOT/Codebase/Setup/configure_systemctl.sh"

echo "----------------------------------------------------"
echo "Setup complete."
echo "Then run './run.sh' to begin."
