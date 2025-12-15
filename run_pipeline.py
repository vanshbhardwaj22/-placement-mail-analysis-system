#!/usr/bin/env python3
"""
Placement Mail Analysis System - Pipeline Orchestrator
Runs all 6 phases sequentially with error handling and progress tracking.
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"pipeline_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Phase definitions
PHASES = [
    {
        "name": "Phase 1: Email Extraction",
        "notebook": "phases/Phase 1/data_extracting.ipynb",
        "output": "phases/Phase 1/placement_emails.csv",
        "description": "Extract emails from Gmail API"
    },
    {
        "name": "Phase 2: Data Cleaning",
        "notebook": "phases/Phase 2/data_cleaning.ipynb",
        "output": "phases/Phase 2/ai_cleaned_emails.csv",
        "description": "Clean email content with AI"
    },
    {
        "name": "Phase 2: Data Filtering",
        "notebook": "phases/Phase 2/data_filtering.ipynb",
        "output": "phases/Phase 2/relevant_placement_emails.csv",
        "description": "Filter relevant placement emails"
    },
    {
        "name": "Phase 3: Entity Structuring",
        "notebook": "phases/Phase 3/entity_structuring.ipynb",
        "output": "phases/Phase 3/structured_job_postings.json",
        "description": "Extract structured job information"
    },
    {
        "name": "Phase 4: Job Prioritization",
        "notebook": "phases/Phase 4/job_prioritization.ipynb",
        "output": "phases/Phase 4/prioritized_jobs.csv",
        "description": "Rank and prioritize job opportunities"
    },
    {
        "name": "Phase 5: PDF Management",
        "notebook": "phases/Phase 5/PDF_Management.ipynb",
        "output": "phases/Phase 5/pdf_metadata.json",
        "description": "Process and index PDF documents"
    },
    {
        "name": "Phase 5: RAG System",
        "notebook": "phases/Phase 5/RAG_System.ipynb",
        "output": "phases/Phase 5/vector_db",
        "description": "Build vector database for Q&A"
    },
    {
        "name": "Phase 6: Excel Reports",
        "notebook": "phases/Phase 6/Excel_Integrate.ipynb",
        "output": "phases/Phase 6/excel_reports",
        "description": "Generate formatted Excel reports"
    }
]


def check_prerequisites():
    """Check if required tools and files exist."""
    logger.info("Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 12):
        logger.error(f"Python 3.12+ required, found {sys.version}")
        return False
    
    # Check jupyter
    try:
        result = subprocess.run(
            ["jupyter", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Jupyter found: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Jupyter not found. Install with: pip install jupyter")
        return False
    
    # Check if Phase 1 has credentials
    creds_file = Path("phases/Phase 1/credentials.json")
    if not creds_file.exists():
        logger.warning(f"Gmail credentials not found at {creds_file}")
        logger.warning("Phase 1 will require manual authentication")
    
    return True


def run_notebook(notebook_path: str, phase_name: str) -> bool:
    """Execute a Jupyter notebook using nbconvert."""
    logger.info(f"Starting: {phase_name}")
    logger.info(f"Notebook: {notebook_path}")
    
    if not Path(notebook_path).exists():
        logger.error(f"Notebook not found: {notebook_path}")
        return False
    
    try:
        # Run notebook with nbconvert
        cmd = [
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            "--ExecutePreprocessor.timeout=600",
            notebook_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info(f"[OK] Completed: {phase_name}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"[FAILED] {phase_name}")
        logger.error(f"Error: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"[FAILED] Unexpected error in {phase_name}: {e}")
        return False


def verify_output(output_path: str) -> bool:
    """Check if expected output file/folder exists."""
    path = Path(output_path)
    exists = path.exists()
    
    if exists:
        if path.is_file():
            size = path.stat().st_size
            logger.info(f"  Output verified: {output_path} ({size:,} bytes)")
        else:
            logger.info(f"  Output verified: {output_path} (directory)")
    else:
        logger.warning(f"  Output not found: {output_path}")
    
    return exists


def run_pipeline(start_phase: int = 1, end_phase: int = None):
    """Run the complete pipeline or specific phases."""
    if not check_prerequisites():
        logger.error("Prerequisites check failed. Aborting.")
        return False
    
    if end_phase is None:
        end_phase = len(PHASES)
    
    logger.info("=" * 70)
    logger.info("PLACEMENT MAIL ANALYSIS SYSTEM - PIPELINE EXECUTION")
    logger.info("=" * 70)
    logger.info(f"Running phases {start_phase} to {end_phase}")
    logger.info(f"Log file: {log_file}")
    logger.info("")
    
    phases_to_run = PHASES[start_phase-1:end_phase]
    completed = 0
    failed = 0
    
    for i, phase in enumerate(phases_to_run, start=start_phase):
        logger.info(f"\n{'='*70}")
        logger.info(f"PHASE {i}/{len(PHASES)}: {phase['name']}")
        logger.info(f"{'='*70}")
        logger.info(f"Description: {phase['description']}")
        
        # Run the notebook
        success = run_notebook(phase['notebook'], phase['name'])
        
        if success:
            # Verify output
            verify_output(phase['output'])
            completed += 1
        else:
            failed += 1
            logger.error(f"\nPhase {i} failed. Check logs for details.")
            
            # Ask if user wants to continue
            response = input("\nContinue to next phase? (y/n): ").strip().lower()
            if response != 'y':
                logger.info("Pipeline execution stopped by user.")
                break
    
    # Summary
    logger.info(f"\n{'='*70}")
    logger.info("PIPELINE EXECUTION SUMMARY")
    logger.info(f"{'='*70}")
    logger.info(f"Completed: {completed}/{len(phases_to_run)}")
    logger.info(f"Failed: {failed}/{len(phases_to_run)}")
    logger.info(f"Log file: {log_file}")
    logger.info(f"{'='*70}\n")
    
    return failed == 0


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run the Placement Mail Analysis System pipeline"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Starting phase number (1-8)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="Ending phase number (1-8)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all phases and exit"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("\nAvailable Phases:")
        print("=" * 70)
        for i, phase in enumerate(PHASES, 1):
            print(f"{i}. {phase['name']}")
            print(f"   {phase['description']}")
            print(f"   Notebook: {phase['notebook']}")
            print(f"   Output: {phase['output']}")
            print()
        sys.exit(0)
    
    success = run_pipeline(args.start, args.end)
    sys.exit(0 if success else 1)
