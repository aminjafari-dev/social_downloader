@echo off
echo ========================================
echo Fixing NumPy Installation on Windows
echo ========================================
echo.

echo This script will fix NumPy compilation issues on Windows.
echo.

echo Step 1: Updating pip...
python -m pip install --upgrade pip

echo.
echo Step 2: Installing NumPy using pre-compiled wheel...
python -m pip install numpy --only-binary=all --upgrade --force-reinstall

if %errorlevel% equ 0 (
    echo.
    echo ✅ NumPy installed successfully!
    echo.
    echo You can now run the main setup script:
    echo setup_windows.bat
) else (
    echo.
    echo ❌ NumPy installation failed.
    echo.
    echo Try running the advanced setup script:
    echo setup_windows_advanced.bat
)

echo.
pause


