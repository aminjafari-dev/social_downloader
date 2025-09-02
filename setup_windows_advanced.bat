@echo off
echo ========================================
echo Social Downloader - Advanced Windows Setup
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
echo Updating pip and setuptools...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing packages using Windows-optimized method...
echo This may take a few minutes...
echo.

echo Step 1: Installing NumPy (pre-compiled wheel)...
python -m pip install numpy --only-binary=all --no-cache-dir

if %errorlevel% neq 0 (
    echo.
    echo Trying alternative NumPy installation...
    python -m pip install numpy --upgrade --force-reinstall --no-cache-dir
)

echo.
echo Step 2: Installing other packages...
python -m pip install yt-dlp requests colorama selenium webdriver-manager openpyxl fake-useragent pillow --no-cache-dir

echo.
echo Step 3: Installing OpenCV (this may take a while)...
python -m pip install opencv-python --only-binary=all --no-cache-dir

if %errorlevel% neq 0 (
    echo.
    echo Trying alternative OpenCV installation...
    python -m pip install opencv-python --upgrade --force-reinstall --no-cache-dir
)

echo.
echo ========================================
echo Setup completed!
echo ========================================
echo.
echo You can now run the application using:
echo - Double-click start_windows.bat
echo - Or run: python src/run.py
echo.
echo If you encounter any issues, try running:
echo python verify_installation.py
echo.
pause


