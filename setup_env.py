#!/usr/bin/env python3
"""
Setup script for Placement Mail Analysis System.
Helps users configure their environment.
"""

import os
import sys
import shutil


def main():
    print("=" * 60)
    print("Placement Mail Analysis System - Setup")
    print("=" * 60)
    print()

    # Check Python version
    if sys.version_info < (3, 12):
        print(f"[WARNING] Python 3.12+ recommended. You have {sys.version}")
    else:
        print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Check for .env file
    if os.path.exists('.env'):
        print("[OK] .env file exists")
    else:
        print("[WARNING] .env file not found")
        
        if os.path.exists('.env.example'):
            response = input("   Create .env from .env.example? (y/n): ").strip().lower()
            if response == 'y':
                shutil.copy('.env.example', '.env')
                print("   [OK] Created .env file")
                print("   Edit .env and add your GEMINI_API_KEY")
                print("   Get free key at: https://aistudio.google.com/apikey")
        else:
            print("   Creating .env template...")
            with open('.env', 'w') as f:
                f.write("# Get your API key at: https://aistudio.google.com/apikey\n")
                f.write("GEMINI_API_KEY=your_api_key_here\n")
            print("   [OK] Created .env file - add your API key!")

    # Check for virtual environment
    if os.path.exists('.venv'):
        print("[OK] Virtual environment exists")
    else:
        print("[WARNING] Virtual environment not found")
        print("   Run: uv sync (or python -m venv .venv)")

    # Check for job data
    jobs_path = "phases/Phase 4/prioritized_jobs.csv"
    if os.path.exists(jobs_path):
        import pandas as pd
        df = pd.read_csv(jobs_path)
        print(f"[OK] Job data found ({len(df)} jobs)")
    else:
        print("[WARNING] Job data not found")
        print("   Run the pipeline first to extract and process emails")

    # Check Gmail credentials
    creds_path = "phases/Phase 1/credentials.json"
    if os.path.exists(creds_path):
        print("[OK] Gmail credentials found")
    else:
        print("[WARNING] Gmail credentials not found")
        print("   See README.md for Gmail API setup instructions")

    print()
    print("=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print()
    
    if not os.path.exists('.env') or 'your_api_key' in open('.env').read():
        print("1. Add your Gemini API key to .env file")
        print("   Get free key: https://aistudio.google.com/apikey")
        print()
    
    print("2. Install dependencies: uv sync")
    print("3. Run web interface: python run_web.py")
    print("4. Open browser: http://localhost:8000")
    print()


if __name__ == "__main__":
    main()
