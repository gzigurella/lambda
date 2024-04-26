#!/bin/bash

# Define accepted versions (modify as needed)
ACCEPTED_VERSIONS="3.7 3.8 3.9 3.10 3.11"

# Check if python command exists
if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: Python is not installed."
  exit 1
fi

# Get python version using IFS and cut
python_version=$(python3 --version 2>&1 | cut -d ' ' -f2 | cut -d '.' -f -2)

# Check if version is in the accepted list
if [[ ! " $ACCEPTED_VERSIONS " =~ " $python_version " ]]; then
  echo "Error: Python version $python_version is not supported. Accepted versions: $ACCEPTED_VERSIONS"
  exit 1
fi

# Python version is accepted, continue script logic here (if any)
echo "Python version $python_version is usable for compilation."

alias python3.11=python3

# Install requirements and compile to binary
python3.11 -m pip install -r requirements.txt
python3.11 -m nuitka --standalone --onefile --follow-imports src/main.py -o lambda

# Cleanup build folders
rm -rf main.build
rm -rf main.dist
rm -rf main.onefile-build