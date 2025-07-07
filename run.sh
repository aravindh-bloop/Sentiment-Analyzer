#!/bin/bash

echo "============================================================"
echo "   🧠 SENTIMENT ANALYSIS TOOL - UNIX/LINUX LAUNCHER"
echo "============================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Error: Python is not installed"
        echo "Please install Python 3.7+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Display Python version
echo "✅ Python is installed"
$PYTHON_CMD --version

# Check if required packages are installed
echo
echo "📋 Checking dependencies..."
$PYTHON_CMD -c "import flask, textblob" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Missing dependencies. Running installation..."
    $PYTHON_CMD install.py
    if [ $? -ne 0 ]; then
        echo "❌ Installation failed"
        exit 1
    fi
fi

# Make run.py executable
chmod +x run.py

# Run the application
echo
echo "🚀 Starting Sentiment Analysis Tool..."
echo "Access the tool at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo

$PYTHON_CMD run.py