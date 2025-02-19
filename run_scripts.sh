#!/bin/bash

# Script to run Python scripts: load_data_postgres.py and transform_data.py

# Load environment variables if .env file exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(cat .env | xargs)
fi

# Function to run a Python script
run_python_script() {
    echo "Running $1..."
    python $1
    if [ $? -eq 0 ]; then
        echo "$1 completed successfully."
    else
        echo "Error: $1 failed to run."
        exit 1
    fi
}

# Run the Python scripts
run_python_script "load_data_postgres.py"
run_python_script "transform_data.py"

echo "All scripts executed successfully."