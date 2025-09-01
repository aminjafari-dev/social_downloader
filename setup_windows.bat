@echo off
echo ========================================
echo Social Downloader - Windows Setup
echo ========================================
echo.

echo Checking if Python is installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first.
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
) else (
    echo Python is already installed.
    python --version
)

echo.
echo Installing required packages...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Error installing packages. Please try again.
    echo If the problem persists, try running as administrator.
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo Setup completed successfully!
    echo ========================================
    echo.
    echo You can now run the application using:
    echo - Double-click start_windows.bat
    echo - Or run: python src/run.py
    echo.
    pause
)
