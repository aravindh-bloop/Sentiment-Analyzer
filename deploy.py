#!/usr/bin/env python3
"""
Deployment Script for Sentiment Analysis Tool
This script prepares the application for production deployment
"""

import os
import sys
import zipfile
import shutil
from datetime import datetime

def create_deployment_package():
    """Create a deployment package with all necessary files"""
    
    # Define files to include in the package
    files_to_include = [
        'main.py',
        'run.py',
        'install.py',
        'run.sh',
        'run.bat',
        'README.md',
        'LICENSE',
        '.gitignore',
        'replit.md',
        'templates/index.html',
        'templates/result.html'
    ]
    
    # Create deployment directory
    deploy_dir = 'sentiment-analysis-tool-deploy'
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    os.makedirs(f'{deploy_dir}/templates')
    
    print("📦 Creating deployment package...")
    
    # Copy files to deployment directory
    for file_path in files_to_include:
        if os.path.exists(file_path):
            if file_path.startswith('templates/'):
                shutil.copy2(file_path, f'{deploy_dir}/{file_path}')
            else:
                shutil.copy2(file_path, f'{deploy_dir}/')
            print(f"✅ Added {file_path}")
        else:
            print(f"⚠️  Warning: {file_path} not found")
    
    # Create requirements.txt in deployment package
    requirements_content = """Flask==3.0.0
TextBlob==0.18.0
gunicorn==23.0.0
"""
    
    with open(f'{deploy_dir}/requirements.txt', 'w') as f:
        f.write(requirements_content)
    print("✅ Created requirements.txt")
    
    # Create deployment instructions
    deploy_instructions = f"""# Deployment Instructions

## Quick Start
1. Extract all files to a directory
2. Run: python install.py
3. Run: python run.py
4. Open http://localhost:5000

## For Windows Users
- Double-click run.bat

## For Linux/Mac Users
- Run: chmod +x run.sh
- Run: ./run.sh

## Package Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(f'{deploy_dir}/DEPLOYMENT.md', 'w') as f:
        f.write(deploy_instructions)
    print("✅ Created deployment instructions")
    
    # Create ZIP archive
    zip_filename = f'sentiment-analysis-tool-{datetime.now().strftime("%Y%m%d")}.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arc_path)
    
    print(f"📁 Created {zip_filename}")
    
    # Clean up temporary directory
    shutil.rmtree(deploy_dir)
    
    print("\n" + "=" * 60)
    print("   🎉 DEPLOYMENT PACKAGE CREATED!")
    print("=" * 60)
    print(f"Package: {zip_filename}")
    print(f"Size: {os.path.getsize(zip_filename) / 1024:.1f} KB")
    print("\nYou can now:")
    print("1. Send this ZIP file to anyone")
    print("2. Upload to GitHub")
    print("3. Deploy to any Python hosting service")
    print("=" * 60)

if __name__ == '__main__':
    create_deployment_package()
