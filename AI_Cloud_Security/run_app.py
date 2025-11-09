#!/usr/bin/env python3
"""
AI-Powered Cloud Security & Compliance Automation
Startup script for the Flask web application
"""

import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("🛡️  AI-Powered Cloud Security & Compliance Automation")
    print("=" * 60)
    
    # Check if dataset exists
    if not os.path.exists('dataset/cloud_security_data.csv'):
        print("📊 Dataset not found. Creating dataset and training model...")
        subprocess.run([sys.executable, 'main_simple.py'])
    else:
        print("✅ Dataset found!")
    
    # Check if model exists
    if not os.path.exists('model/cloud_model.pkl'):
        print("🤖 Model not found. Training model...")
        subprocess.run([sys.executable, 'main_simple.py'])
    else:
        print("✅ Model found!")
    
    print("\n🚀 Starting Flask web application...")
    print("📱 Open your browser and navigate to: http://127.0.0.1:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Change to app directory and run Flask app
    os.chdir('app')
    subprocess.run([sys.executable, 'app_simple.py'])

if __name__ == "__main__":
    main()