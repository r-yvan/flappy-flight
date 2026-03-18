#!/bin/bash

# ==============================================================================
# Flappy Flight - Quick Start Script
# This script allows you to start the game directly without typing python commands
# ==============================================================================

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo -e "\033[36m[*] Checking system requirements...\033[0m"

# Ensure Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "\033[31m[✗] Python3 could not be found. Please install Python3 to run this game.\033[0m"
    echo -e "    Run: sudo apt-get install python3"
    exit 1
fi

# Ensure pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "\033[33m[!] pip is not installed. Dependency installation might fail.\033[0m"
    echo -e "    Run: sudo apt-get install python3-pip"
fi

# Launch the game
echo -e "\033[32m[✓] Requirements met. Launching Flappy Flight...\033[0m"
python3 launcher.py
