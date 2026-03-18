#!/bin/bash

# ==============================================================================
# Flappy Flight - Quick Start Script (Linux)
# ==============================================================================

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Ensure Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "\033[31m[✗] Python3 could not be found. Please install Python3 to run this game.\033[0m"
    echo -e "    Run: sudo apt-get install python3"
    exit 1
fi

# Launch the game (automatic venv setup handles the rest)
python3 launcher.py
