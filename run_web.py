#!/usr/bin/env python3
"""
Start the web interface for the Job Search Assistant.
"""

import os
import sys


def main():
    # Ensure we're in the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # Check for .env file
    if not os.path.exists('.env'):
        print("[WARNING] .env file not found!")
        print("Create a .env file with: GEMINI_API_KEY=your_api_key")
        print()

    # Check for required data
    jobs_path = "phases/Phase 4/prioritized_jobs.csv"
    if not os.path.exists(jobs_path):
        print(f"[WARNING] Jobs data not found at {jobs_path}")
        print("Run the pipeline first to generate job data.")
        print()

    print("=" * 60)
    print("Starting Job Search Assistant Web Interface")
    print("=" * 60)
    print()
    print("Open your browser at: http://localhost:8000")
    print("API docs available at: http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Start the server
    import uvicorn
    uvicorn.run(
        "web.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
