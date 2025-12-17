# Phase 3: Entity Structuring & Relationship Extraction

## Overview

Phase 3 transforms flat entity strings from Phase 2 into structured job postings with proper relationships and validation. This phase now includes **incremental processing** support and **configuration-driven** behavior.

## New Features

### ✅ Incremental Processing
- Only processes NEW emails (not already processed)
- Maintains state in `state/processed_message_ids.txt`
- Checkpoint system for crash recovery
- Merges new results with existing data
- Significantly faster on subsequent runs

### ✅ Configuration-Driven
- All hardcoded values moved to `config.json`
- Easy customization without code changes
- Validation of configuration on load
- Support for different environments

## Files

### Core Files
- **`entity_structuring_pipeline.py`** - Refactored pipeline with incremental processing
- **`entity_structuring_incremental.ipynb`** - New notebook using the pipeline
- **`entity_structuring.ipynb`** - Original notebook (legacy)
- **`config.json`** - Configuration file with all settings
- **`config_manager.py`** - Configuration management and validation
- **`test_config_manager.py`** - Tests for configuration manager

### Output Files
- **`structured_job_postings.csv`** - Flattened job data
- **`structured_job_postings.json`** - Complete structured data
- **`entity_structuring.log`** - Processing logs

### State Files
- **`state/processed_message_ids.txt`** - Tracks processed emails

## Configuration

All settings are in `config.json`:

```json
{
  "incremental_processing": {
    "enabled": true,
    "state_directory": "state",
    "state_file": "processed_message_ids.txt",
    "checkpoint_interval": 50,
    "force_full_reprocess": false
  },
  "processing": {
    "max_jobs_per_email": 5,
    "min_completeness_score": 0.3,
    "enable_analytics": true,
    "max_companies_per_email": 3,
    "max_positions_per_email": 3
  },
  "normalization": {
    "skill_map": { ... },
    "degree_map": { ... },
    "city_map": { ... },
    "company_suffixes": [ ... ]
  },
  ...
}
```

### Key Configuration Sections

1. **incremental_processing** - Control incremental behavior
2. **input_output** - File paths
3. **processing** - Processing limits and thresholds
4. **logging** - Log levels and files
5. **normalization** - Entity normalization mappings
6. **position_levels** - Keywords for position level detection
7. **work_mode_keywords** - Remote/hybrid detection
8. **experience_types** - Experience level thresholds
9. **salary_parsing** - Salary regex patterns
10. **experience_parsing** - Experience regex patterns
11. **deadline_parsing** - Date parsing patterns

## Usage

### Option 1: Using the Notebook (Recommended)

```python
# Open entity_structuring_incremental.ipynb
# Run all cells
```

### Option 2: Using Python Script

```bash
cd "phases/Phase 3"
python entity_structuring_pipeline.py
```

### Option 3: Programmatic Usage

```python
from entity_structuring_pipeline import EntityStructuringPipeline

# Initialize with config
pipeline = EntityStructuringPipeline("config.json")

# Process dataset (incremental by default)
jobs_df, jobs_list = pipeline.process_dataset()

# Generate analytics
pipeline.generate_analytics()
```

## Incremental Processing Workflow

### First Run
1. Loads all emails from Phase 2
2. Processes all emails
3. Saves results to CSV/JSON
4. Saves processed message IDs to state file

### Subsequent Runs
1. Loads state file (processed message IDs)
2. Filters out already-processed emails
3. Processes ONLY new emails
4. Loads existing results
5. Merges new results with existing
6. Saves updated results
7. Updates state file

### Force Full Reprocessing

To reprocess all emails:

```json
{
  "incremental_processing": {
    "force_full_reprocess": true
  }
}
```

Or delete the state file:
```bash
rm state/processed_message_ids.txt
```

## Customization

### Adding New Skills to Normalize

Edit `config.json`:
```json
{
  "normalization": {
    "skill_map": {
      "your_abbreviation": "full_name",
      "react": "reactjs"
    }
  }
}
```

### Changing Processing Limits

```json
{
  "processing": {
    "max_jobs_per_email": 10,
    "max_companies_per_email": 5,
    "max_positions_per_email": 5
  }
}
```

### Adding Salary Patterns

```json
{
  "salary_parsing": {
    "patterns": [
      {
        "name": "your_pattern",
        "pattern": "regex_here",
        "confidence": 0.85
      }
    ]
  }
}
```

## Performance

### Without Incremental Processing
- First run: ~5-10 minutes for 1000 emails
- Subsequent runs: ~5-10 minutes (reprocesses everything)

### With Incremental Processing
- First run: ~5-10 minutes for 1000 emails
- Subsequent runs: ~30 seconds (only new emails)
- **90% faster** on subsequent runs!

## Checkpoint System

The pipeline saves checkpoints every N emails (default: 50):
- If the process crashes, restart it
- It will resume from the last checkpoint
- No duplicate processing

## Testing

Run configuration tests:
```bash
python test_config_manager.py
```

## Migration from Old Notebook

The old `entity_structuring.ipynb` still works but doesn't have:
- Incremental processing
- Configuration file support
- State management

**Recommended:** Use `entity_structuring_incremental.ipynb` instead.

## Troubleshooting

### "No new emails to process"
- All emails have been processed
- Check `state/processed_message_ids.txt`
- Set `force_full_reprocess: true` to reprocess

### Configuration validation errors
- Check `config.json` syntax
- Ensure all required fields are present
- Run `python test_config_manager.py`

### Missing input file
- Ensure Phase 2 has been run
- Check `input_file` path in config
- Path is relative to Phase 3 directory

## Output Schema

### CSV Columns
- `job_id`, `email_id`
- `company_name`, `company_canonical`, `company_confidence`
- `position_title`, `position_level`, `position_confidence`
- `skills_required`, `skills_count`, `education_required`
- `experience_min_years`, `experience_max_years`, `experience_type`
- `location_city`, `location_state`, `work_mode`, `location_confidence`
- `salary_min`, `salary_max`, `salary_currency`, `salary_period`
- `application_deadline`, `apply_link`, `contact_email`
- `completeness_score`, `extraction_timestamp`, `source_subject`

### JSON Structure
```json
{
  "job_id": "...",
  "email_id": "...",
  "company": { "name": "...", "canonical_name": "...", "confidence": 0.85 },
  "position": { "title": "...", "level": "...", "confidence": 0.85 },
  "requirements": { "skills": [...], "education": [...], "experience_min": 0, "experience_max": 5 },
  "location": { "city": "...", "state": "...", "work_mode": "...", "confidence": 0.8 },
  "compensation": { "salary_min": 0, "salary_max": 0, "currency": "INR", "period": "annual" },
  "application": { "deadline": "...", "apply_link": "...", "contact_email": "..." },
  "metadata": { "completeness_score": 0.75, "extraction_timestamp": "...", "source_subject": "..." }
}
```

## Next Steps

After Phase 3, proceed to:
- **Phase 4**: Job Prioritization
- **Phase 5**: RAG System & Conversational Agent
- **Phase 6**: Excel Report Generation
