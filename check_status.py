#!/usr/bin/env python3
"""Check the status of all pipeline phases."""

from pathlib import Path
from datetime import datetime

PHASES = [
    ("Phase 1", "phases/Phase 1/placement_emails.csv", "Email extraction"),
    ("Phase 2 (Clean)", "phases/Phase 2/ai_cleaned_emails.csv", "Data cleaning"),
    ("Phase 2 (Filter)", "phases/Phase 2/relevant_placement_emails.csv", "Data filtering"),
    ("Phase 3", "phases/Phase 3/structured_job_postings.json", "Entity structuring"),
    ("Phase 4", "phases/Phase 4/prioritized_jobs.csv", "Job prioritization"),
    ("Phase 5 (PDF)", "phases/Phase 5/pdf_metadata.json", "PDF management"),
    ("Phase 5 (RAG)", "phases/Phase 5/vector_db", "RAG system"),
    ("Phase 6", "phases/Phase 6/excel_reports", "Excel reports"),
]

print("\n" + "=" * 70)
print("PLACEMENT MAIL ANALYSIS SYSTEM - PIPELINE STATUS")
print("=" * 70 + "\n")

completed = 0
for phase_name, output_path, description in PHASES:
    path = Path(output_path)
    status = "[OK]" if path.exists() else "[--]"
    
    if path.exists():
        completed += 1
        if path.is_file():
            size = path.stat().st_size
            mod_time = datetime.fromtimestamp(path.stat().st_mtime)
            info = f"({size:,} bytes, modified {mod_time.strftime('%Y-%m-%d %H:%M')})"
        else:
            info = "(directory exists)"
    else:
        info = "(not found)"
    
    print(f"{status} {phase_name:20} {description:25} {info}")

print(f"\n{'=' * 70}")
print(f"Progress: {completed}/{len(PHASES)} phases completed")
print(f"{'=' * 70}\n")
