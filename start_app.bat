@echo off
echo Setting up VaaniMitra to use E drive for model storage...

REM Check if E drive exists
if not exist "E:\" (
    echo ERROR: E drive not found! Please ensure E drive is available.
    echo You can modify this script to use a different drive letter.
    pause
    exit /b 1
)

REM Set HuggingFace environment variables to use E drive
set HF_HOME=E:\VaaniMitraData\cache
set HF_HUB_CACHE=E:\VaaniMitraData\cache
set TRANSFORMERS_CACHE=E:\VaaniMitraData\cache

REM Create directories if they don't exist
if not exist "E:\VaaniMitraData\cache" mkdir "E:\VaaniMitraData\cache"
if not exist "E:\VaaniMitraData\models" mkdir "E:\VaaniMitraData\models"

echo Environment configured successfully!
echo Models will be stored in: E:\VaaniMitraData\models\
echo Cache will be stored in: E:\VaaniMitraData\cache\
echo.
echo Note: First run may take time to download AI models (~1GB)
echo Subsequent runs will be faster as models are cached.
echo.

REM Start the Flask app
echo Starting VaaniMitra...
python app.py