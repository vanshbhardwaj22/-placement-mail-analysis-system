"""
Incremental State Management for Phase 2 Data Cleaning
This module provides functions to track processed emails and enable incremental processing.
"""

import os
import logging
from typing import Set

logger = logging.getLogger("AI_Cleaning")


def load_processed_ids(state_file: str) -> Set[str]:
    """
    Load already processed message IDs from state file.
    
    Args:
        state_file: Path to the state file
        
    Returns:
        Set of processed message IDs
    """
    if not os.path.exists(state_file):
        logger.info(f"No existing state file found at {state_file}")
        return set()
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            processed_ids = {line.strip() for line in f if line.strip()}
        logger.info(f"Loaded {len(processed_ids)} processed message IDs from state")
        return processed_ids
    except Exception as e:
        logger.warning(f"Failed to load state file {state_file}: {e}")
        return set()


def save_processed_ids(state_file: str, new_ids: Set[str]) -> None:
    """
    Append new processed IDs to existing set and persist to disk.
    
    Args:
        state_file: Path to the state file
        new_ids: Set of new message IDs to save
    """
    # Load existing IDs
    existing_ids = load_processed_ids(state_file)
    
    # Merge with new IDs
    merged_ids = existing_ids.union(new_ids)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(state_file) or ".", exist_ok=True)
    
    try:
        # Write to temp file first (atomic write)
        temp_file = state_file + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            for msg_id in sorted(merged_ids):
                f.write(f"{msg_id}\n")
        
        # Rename temp file to actual file (atomic operation)
        if os.path.exists(state_file):
            os.remove(state_file)
        os.rename(temp_file, state_file)
        
        logger.info(f"Saved {len(merged_ids)} total processed IDs to state ({len(new_ids)} new)")
    except Exception as e:
        logger.error(f"Failed to save state file {state_file}: {e}")
        # Clean up temp file if it exists
        if os.path.exists(temp_file):
            os.remove(temp_file)


def get_checkpoint_file(state_dir: str) -> str:
    """Get path to checkpoint file for recovery."""
    return os.path.join(state_dir, "checkpoint.txt")


def save_checkpoint(state_dir: str, processed_ids: Set[str]) -> None:
    """Save checkpoint for crash recovery."""
    checkpoint_file = get_checkpoint_file(state_dir)
    os.makedirs(state_dir, exist_ok=True)
    
    try:
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            for msg_id in sorted(processed_ids):
                f.write(f"{msg_id}\n")
        logger.debug(f"Checkpoint saved: {len(processed_ids)} IDs")
    except Exception as e:
        logger.warning(f"Failed to save checkpoint: {e}")


def load_checkpoint(state_dir: str) -> Set[str]:
    """Load checkpoint for crash recovery."""
    checkpoint_file = get_checkpoint_file(state_dir)
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                ids = {line.strip() for line in f if line.strip()}
            logger.info(f"Loaded checkpoint: {len(ids)} IDs")
            return ids
        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}")
    return set()


def clear_checkpoint(state_dir: str) -> None:
    """Clear checkpoint file after successful completion."""
    checkpoint_file = get_checkpoint_file(state_dir)
    if os.path.exists(checkpoint_file):
        try:
            os.remove(checkpoint_file)
            logger.debug("Checkpoint cleared")
        except Exception as e:
            logger.warning(f"Failed to clear checkpoint: {e}")
