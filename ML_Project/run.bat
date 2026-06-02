@echo off
SETLOCAL EnableDelayedExpansion
title BioShield Crop Diagnostics - Server Launcher

echo =====================================================================
echo 🌾 BioShield Crop Diagnostics Launcher (Windows Host Environment) 🌾
echo =====================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not added to your system PATH.
    echo Please install Python 3.8+ from https://www.python.org/ and try again.
    echo.
    pause
    exit /b 1
)

:: Set up virtual environment
if not exist .venv (
    echo 📦 Virtual environment '.venv' not found. Creating virtual environment...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo ❌ Error creating virtual environment.
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created successfully.
    echo.
)

:: Activate virtual environment
echo 🔌 Activating Python virtual environment...
call .venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b 1
)
echo.

:: Choice of installation dependencies
echo 🛠️  Select your desired backend execution mode:
echo   [1] Lightweight Simulation Mode (Installs web server and Pillow. Takes ^<30 seconds)
echo   [2] Full ML PyTorch Inference (Installs web server, Pillow, PyTorch, and Torchvision. Takes a few minutes)
echo.
set /p mode="Enter choice [1 or 2] (Default is 1): "

if "%mode%"=="2" (
    echo.
    echo ⚙️ Installing full ML dependencies (including CPU-inference PyTorch)...
    pip install fastapi uvicorn python-multipart pillow torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
) else (
    echo.
    echo ⚙️ Installing lightweight dependencies (FastAPI, Uvicorn, Pillow)...
    pip install fastapi uvicorn python-multipart pillow
)

if !errorlevel! neq 0 (
    echo.
    echo ❌ Error occurred during dependency installation. Please check your internet connection.
    pause
    exit /b 1
)
echo.
echo ✅ Dependency configuration verified.

:: Start browser in background
echo 🌐 Launching default web browser to: http://localhost:8000
start http://localhost:8000

:: Run backend FastAPI server
echo.
echo 🚀 Launching Uvicorn server...
echo Press Ctrl+C to terminate the application.
echo.
uvicorn app:app --reload --host 127.0.0.1 --port 8000

pause
