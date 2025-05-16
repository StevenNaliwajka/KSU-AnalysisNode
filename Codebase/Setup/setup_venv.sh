#!/bin/bash

echo "Setting up Python virtual environment..."

# Parse -venv flag if passed
CUSTOM_VENV=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -venv)
      CUSTOM_VENV="$2"
      shift 2
      ;;
    *)
      echo "(setup_venv.sh) Unknown option: $1"
      exit 1
      ;;
  esac
done

# Resolve script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/../.."

# Determine venv path: use passed path or default
if [ -n "$CUSTOM_VENV" ]; then
  VENV_DIR="$CUSTOM_VENV"
  echo "(setup_venv.sh) Using custom virtual environment path: $VENV_DIR"
else
  VENV_DIR="$PROJECT_ROOT/venv"
  echo "(setup_venv.sh) Using default virtual environment path: $VENV_DIR"
fi

REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

# Check for Python3
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 is not installed. Please run install_python.sh first."
  exit 1
fi

# Check for ensurepip
if python3 -c "import ensurepip" 2>/dev/null; then
  echo "ensurepip is available."
else
  echo "ensurepip not found. Installing python3-venv and python3-pip..."
  sudo apt update
  sudo apt install -y python3-venv python3-pip
  if python3 -c "import ensurepip" 2>/dev/null; then
    echo "ensurepip installed."
  else
    echo "Failed to install ensurepip."
    exit 1
  fi
fi

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at: $VENV_DIR"
  python3 -m venv "$VENV_DIR"
else
  echo "Virtual environment already exists at: $VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install requirements
if [ -f "$REQUIREMENTS_FILE" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install --upgrade pip
  pip install -r "$REQUIREMENTS_FILE"
  echo "Dependencies installed."
else
  echo "No requirements.txt found at: $REQUIREMENTS_FILE"
fi
