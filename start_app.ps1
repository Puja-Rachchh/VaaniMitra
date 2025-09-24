# VaaniMitra Startup Script
# Configures the app to use E drive for model storage

Write-Host "Setting up VaaniMitra to use E drive for model storage..." -ForegroundColor Green

# Check if E drive exists
if (!(Test-Path "E:\")) {
    Write-Host "ERROR: E drive not found! Please ensure E drive is available." -ForegroundColor Red
    Write-Host "You can modify this script to use a different drive letter." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Set HuggingFace environment variables to use E drive
$env:HF_HOME = "E:\VaaniMitraData\cache"
$env:HF_HUB_CACHE = "E:\VaaniMitraData\cache"
$env:TRANSFORMERS_CACHE = "E:\VaaniMitraData\cache"

# Create directories if they don't exist
if (!(Test-Path "E:\VaaniMitraData\cache")) {
    New-Item -ItemType Directory -Path "E:\VaaniMitraData\cache" -Force
}
if (!(Test-Path "E:\VaaniMitraData\models")) {
    New-Item -ItemType Directory -Path "E:\VaaniMitraData\models" -Force
}

Write-Host "Environment configured successfully!" -ForegroundColor Green
Write-Host "Models will be stored in: E:\VaaniMitraData\models\" -ForegroundColor Yellow
Write-Host "Cache will be stored in: E:\VaaniMitraData\cache\" -ForegroundColor Yellow
Write-Host ""
Write-Host "Note: First run may take time to download AI models (~1GB)" -ForegroundColor Cyan
Write-Host "Subsequent runs will be faster as models are cached." -ForegroundColor Cyan
Write-Host ""

# Start the Flask app
Write-Host "Starting VaaniMitra..." -ForegroundColor Green
python app.py