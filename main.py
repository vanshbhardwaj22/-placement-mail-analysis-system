#!/usr/bin/env python3
"""
Placement Mail Analysis System
==============================
An AI-powered system for extracting, analyzing, and prioritizing 
job opportunities from placement emails.

Author: Vansh Bhardwaj
License: MIT
"""

import sys


def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("Placement Mail Analysis System")
    print("=" * 60)
    print()
    print("Available commands:")
    print()
    print("  python run_web.py      - Start web interface")
    print("  python run_pipeline.py - Run data pipeline")
    print("  python setup_env.py    - Setup environment")
    print("  python check_status.py - Check pipeline status")
    print()
    print("Web Interface: http://localhost:8000")
    print("API Docs:      http://localhost:8000/docs")
    print()
    print("=" * 60)
    
    # Check if user wants to start web server
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        from run_web import main as run_web
        run_web()


if __name__ == "__main__":
    main()
