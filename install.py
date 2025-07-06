#!/usr/bin/env python3
"""
Installation Script for Sentiment Analysis Tool
This script handles the installation and setup of dependencies
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")

def install_package(package):
    """Install a Python package using pip"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def check_package_installed(package):
    """Check if a package is already installed"""
    return importlib.util.find_spec(package) is not None

def download_nltk_data():
    """Download required NLTK data for TextBlob"""
    try:
        print("📚 Downloading language data...")
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True)
        print("✅ Language data downloaded successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not download language data: {e}")
        print("   TextBlob will still work but might be less accurate")

def main():
    """Main installation function"""
    print("=" * 60)
    print("   🧠 SENTIMENT ANALYSIS TOOL - INSTALLER")
    print("=" * 60)
    
    # Check Python version
    check_python_version()
    
    # List of required packages
    packages = [
        'flask',
        'textblob',
        'gunicorn'
    ]
    
    print("\n📋 Installing required packages...")
    
    # Install packages
    success_count = 0
    for package in packages:
        if check_package_installed(package):
            print(f"✅ {package} is already installed")
            success_count += 1
        else:
            if install_package(package):
                success_count += 1
    
    if success_count == len(packages):
        print("\n🎉 All packages installed successfully!")
        
        # Download NLTK data
        download_nltk_data()
        
        print("\n" + "=" * 60)
        print("   🚀 INSTALLATION COMPLETE!")
        print("=" * 60)
        print("To run the application:")
        print("1. python run.py")
        print("2. Open http://localhost:5000 in your browser")
        print("=" * 60)
    else:
        print(f"\n❌ Installation failed for {len(packages) - success_count} packages")
        print("Please check your internet connection and try again")
        sys.exit(1)

if __name__ == '__main__':
    main()