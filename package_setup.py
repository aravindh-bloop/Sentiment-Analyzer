#!/usr/bin/env python3
"""
Sentiment Analysis Tool - Complete Package Setup
This script creates a downloadable package with all project files
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_package():
    """Create a complete downloadable package"""
    package_name = f"sentiment-analysis-tool-complete-{datetime.now().strftime('%Y%m%d')}"
    
    # Create package directory
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Files to include in package
    files_to_copy = [
        'main.py',
        'requirements.txt',
        'runtime.txt',
        'Procfile',
        'render.yaml',
        'README.md',
        'LICENSE',
        'install.py',
        'run.py',
        'run.sh',
        'run.bat',
        'deploy.py',
        'replit.md',
        '.gitignore'
    ]
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_name)
            print(f"✓ Copied {file}")
    
    # Copy templates directory
    if os.path.exists('templates'):
        shutil.copytree('templates', os.path.join(package_name, 'templates'))
        print("✓ Copied templates directory")
    
    # Create zip file
    zip_filename = f"{package_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arcname)
    
    # Clean up temporary directory
    shutil.rmtree(package_name)
    
    print(f"\n✅ Package created: {zip_filename}")
    print(f"📦 Size: {os.path.getsize(zip_filename) / 1024:.1f} KB")
    return zip_filename

if __name__ == "__main__":
    create_package()