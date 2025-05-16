#!/bin/bash

echo "Installing Python and pip..."

if ! command -v python3 >/dev/null 2>&1; then
  echo "Installing Python3..."
  sudo apt update
  sudo apt install -y python3
else
  echo "Python3 is already installed."
fi

if ! command -v pip3 >/dev/null 2>&1; then
  echo "Installing pip3..."
  sudo apt install -y python3-pip
else
  echo "pip3 is already installed."
fi

python3 --version
pip3 --version
