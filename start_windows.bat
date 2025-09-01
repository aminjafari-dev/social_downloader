@echo off
echo ========================================
echo Social Downloader - Starting Application
echo ========================================
echo.

echo Checking if Python is installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please run setup_windows.bat first.
    pause
    exit /b 1
)

echo Starting Social Downloader...
echo.

cd /d "%~dp0"
python src/run.py

if %errorlevel% neq 0 (
    echo.
    echo Error starting the application.
    echo Please make sure you have run setup_windows.bat first.
    pause
)
