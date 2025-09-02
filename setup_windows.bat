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
echo Updating pip and setuptools...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing required packages...
echo This may take a few minutes...
echo.

echo Installing NumPy first (this may take a while)...
python -m pip install numpy --only-binary=all

if %errorlevel% neq 0 (
    echo.
    echo Warning: NumPy installation failed. Trying alternative method...
    python -m pip install numpy --upgrade --force-reinstall
)

echo.
echo Installing remaining packages...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Some packages failed to install. Trying individual installation...
    echo.
    
    echo Installing yt-dlp...
    python -m pip install yt-dlp
    
    echo Installing requests...
    python -m pip install requests
    
    echo Installing colorama...
    python -m pip install colorama
    
    echo Installing selenium...
    python -m pip install selenium
    
    echo Installing webdriver-manager...
    python -m pip install webdriver-manager
    
    echo Installing openpyxl...
    python -m pip install openpyxl
    
    echo Installing fake-useragent...
    python -m pip install fake-useragent
    
    echo Installing opencv-python...
    python -m pip install opencv-python
    
    echo Installing pillow...
    python -m pip install pillow
    
    echo.
    echo Individual package installation completed.
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
