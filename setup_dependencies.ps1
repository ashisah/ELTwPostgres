# Load environment variables if .env file exists
if (Test-Path .env) {
    Write-Host "Loading environment variables from .env file..."
    Get-Content .env | ForEach-Object {
        $name, $value = $_.Split('=', 2)
        Set-Item -Path "Env:$name" -Value $value
    }
}

# Function to check if a package is installed
function Is-Package-Installed {
    param ($package)
    try {
        python -c "import $package" 2>&1 | Out-Null
        Write-Host "$package is already installed."
        return $true
    } catch {
        Write-Host "$package is not installed."
        return $false
    }
}

# List of required packages
$REQUIRED_PACKAGES = @("psycopg2", "pandas", "python-dotenv")

# Check and install each package
foreach ($PACKAGE in $REQUIRED_PACKAGES) {
    if (-not (Is-Package-Installed $PACKAGE)) {
        Write-Host "Installing $PACKAGE..."
        pip install $PACKAGE
    }
}

Write-Host "All dependencies are installed."