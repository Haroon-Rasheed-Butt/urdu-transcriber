@echo off
REM Windows Setup Script for Urdu Meeting Transcriber
REM Run this file to set up everything automatically

echo ============================================================
echo    Urdu Meeting Transcriber - Automated Setup
echo ============================================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.9 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing required packages...
echo This may take 5-10 minutes on first run...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Package installation failed
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo.

REM Create necessary directories
echo Creating directories...
if not exist "audio" mkdir audio
if not exist "output" mkdir output
echo.

REM Run system test
echo Running system compatibility test...
echo.
python test_setup.py
if %errorlevel% neq 0 (
    echo.
    echo WARNING: System test encountered issues
    echo Please review the output above
    echo.
)

echo.
echo ============================================================
echo    Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Place your audio file in the project folder
echo 2. Run: python transcribe.py your_audio.mp3
echo 3. Wait for processing to complete
echo 4. Copy the Claude prompt and paste into Claude
echo.
echo For detailed instructions, see README.md or QUICKSTART.md
echo.
pause
