#!/usr/bin/env python3
"""
Clear all Jupyter notebook outputs before committing to GitHub.
Removes personal data from cell outputs.
"""

import subprocess
from pathlib import Path


def clear_notebooks():
    print("Clearing notebook outputs...")
    
    notebooks = list(Path("phases").rglob("*.ipynb"))
    
    for nb in notebooks:
        print(f"  Clearing: {nb}")
        subprocess.run([
            "jupyter", "nbconvert",
            "--clear-output", "--inplace",
            str(nb)
        ], capture_output=True)
    
    print(f"\n[OK] Cleared {len(notebooks)} notebooks")
    print("Safe to commit to GitHub!")


if __name__ == "__main__":
    clear_notebooks()
