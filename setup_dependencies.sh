#!/bin/bash

# Script to check and install required Python packages

# Load environment variables if .env file exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(cat .env | xargs)
fi

# Function to check if a package is installed
is_package_installed() {
    python -c "import $1" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "$1 is already installed."
        return 0
    else
        echo "$1 is not installed."
        return 1
    fi
}

# List of required packages
REQUIRED_PACKAGES=("psycopg2" "pandas" "python-dotenv")

# Check and install each package
for PACKAGE in "${REQUIRED_PACKAGES[@]}"; do
    if ! is_package_installed $PACKAGE; then
        echo "Installing $PACKAGE..."
        pip install $PACKAGE
    fi
done

echo "All dependencies are installed."