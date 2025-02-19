# Load environment variables if .env file exists
if (Test-Path .env) {
    Write-Host "Loading environment variables from .env file..."
    Get-Content .env | ForEach-Object {
        $name, $value = $_.Split('=', 2)
        Set-Item -Path "Env:$name" -Value $value
    }
}

# Function to run a Python script
function Run-Python-Script {
    param ($script)
    Write-Host "Running $script..."
    python $script
    if ($LASTEXITCODE -eq 0) {
        Write-Host "$script completed successfully."
    } else {
        Write-Host "Error: $script failed to run."
        exit 1
    }
}

# Run the Python scripts
Run-Python-Script "load_data_postgres.py"
Run-Python-Script "transform_data.py"

Write-Host "All scripts executed successfully."