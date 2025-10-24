@echo off
title Clinic Management System
echo ========================================
echo    Clinic Management System
echo    Starting Application...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Checking Python installation...
python --version
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo First time setup - Installing required packages...
    echo This may take a few minutes...
    echo.
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo.
    echo Installation complete!
    echo.
)

REM Check if database exists
if not exist "instance" mkdir instance
if not exist "instance\clinic.db" (
    echo Creating database for first time...
    python seed.py
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to create database!
        echo Please check the error messages above.
        pause
        exit /b 1
    )
    echo Database created successfully!
    echo.
)

REM Start the application
echo ========================================
echo Starting Clinic Management System...
echo ========================================
echo.
echo The system is now running!
echo.
echo Please open your web browser and go to:
echo.
echo    http://127.0.0.1:5000
echo.
echo Login with these credentials:
echo    Username: doctor
echo    Password: password
echo.
echo IMPORTANT: Keep this window open while using the system!
echo To stop the server, close this window or press Ctrl+C
echo ========================================
echo.

python app.py

echo.
echo ========================================
echo Server stopped.
echo ========================================
pause

