@echo off
echo ============================================================
echo    🧠 SENTIMENT ANALYSIS TOOL - WINDOWS LAUNCHER
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Display Python version
echo ✅ Python is installed
python --version

REM Check if required packages are installed
echo.
echo 📋 Checking dependencies...
python -c "import flask, textblob" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Missing dependencies. Running installation...
    python install.py
    if %errorlevel% neq 0 (
        echo ❌ Installation failed
        pause
        exit /b 1
    )
)

REM Run the application
echo.
echo 🚀 Starting Sentiment Analysis Tool...
echo Access the tool at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python run.py

pause