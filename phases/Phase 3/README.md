# Phase 3: Entity Structuring & Relationship Extraction

## Overview

Phase 3 transforms flat entity strings from Phase 2 into structured job postings with proper relationships and validation. This phase features **incremental processing** and **configuration-driven** architecture for efficient and customizable entity extraction.

## Key Features

### ✅ Incremental Processing
- **Smart Processing**: Only processes NEW emails that haven't been processed before
- **State Management**: Maintains state in `state/processed_message_ids.txt`
- **Checkpoint System**: Saves progress every 50 emails for crash recovery
- **Result Merging**: Automatically merges new results with existing data
- **Performance**: **90% faster** on subsequent runs

### ✅ Configuration-Driven Architecture
- **Centralized Config**: All settings in `config.json` - no hardcoded values
- **Easy Customization**: Modify behavior without changing code
- **Comprehensive Validation**: Configuration validated on load
- **Rich Mappings**: 
  - 13 skill normalizations (js→javascript, py→python, etc.)
  - 14 degree normalizations (btech→B.Tech, be→B.E, etc.)
  - 15 city normalizations (bangalore→Bangalore, bengaluru→Bangalore, etc.)
  - 9 company suffix removals (PVT LTD, LIMITED, etc.)

### ✅ Advanced Parsing
- **Salary Parsing**: 5 regex patterns for various salary formats (LPA, monthly, CTC, etc.)
- **Experience Parsing**: 3 patterns for experience requirements
- **Deadline Parsing**: 3 date format patterns + relative date support
- **Position Level Detection**: Automatic seniority level classification
- **Work Mode Detection**: Identifies remote, hybrid, and on-site positions

## File Structure

```
phases/Phase 3/
├── entity_structuring.ipynb          # Main notebook (all code in one place)
├── config.json                        # Configuration file (not in git)
├── config_manager.py                  # Configuration management & validation
├── README.md                          # This file
├── state/                             # State directory (not in git)
│   └── processed_message_ids.txt     # Tracks processed emails
├── structured_job_postings.csv        # Output: Flattened data (not in git)
├── structured_job_postings.json       # Output: Complete structure (not in git)
└── entity_structuring.log             # Processing logs (not in git)
```

### Files Excluded from Git
- `config.json` - Contains configuration (use config.example.json as template)
- `*.csv`, `*.json` - Output files
- `*.log` - Log files
- `state/` - State tracking directory

## Quick Start

### 1. Open Jupyter Notebook
```bash
jupyter notebook entity_structuring.ipynb
```

### 2. Run All Cells
The notebook will automatically:
1. Load configuration from `config.json`
2. Check for previously processed emails
3. Process only NEW emails
4. Merge with existing results
5. Save outputs (CSV + JSON)
6. Generate analytics report

### 3. View Results
- **CSV**: `structured_job_postings.csv` - Tabular format (30 columns)
- **JSON**: `structured_job_postings.json` - Complete structured data
- **Log**: `entity_structuring.log` - Detailed processing logs

## Configuration Guide

### Main Configuration Sections

#### 1. Incremental Processing
```json
{
  "incremental_processing": {
    "enabled": true,                    // Enable/disable incremental processing
    "state_directory": "state",         // Directory for state files
    "state_file": "processed_message_ids.txt",  // State file name
    "checkpoint_interval": 50,          // Save checkpoint every N emails
    "force_full_reprocess": false       // Force reprocess all emails
  }
}
```

#### 2. Input/Output
```json
{
  "input_output": {
    "input_file": "../Phase 2/relevant_placement_emails.csv",
    "output_csv": "structured_job_postings.csv",
    "output_json": "structured_job_postings.json"
  }
}
```

#### 3. Processing Limits
```json
{
  "processing": {
    "max_jobs_per_email": 5,            // Max job postings per email
    "max_companies_per_email": 3,       // Max companies to extract per email
    "max_positions_per_email": 3,       // Max positions to extract per email
    "min_completeness_score": 0.3,      // Minimum completeness (0.0-1.0)
    "enable_analytics": true            // Generate analytics report
  }
}
```

#### 4. Normalization Mappings
```json
{
  "normalization": {
    "skill_map": {
      "js": "javascript",
      "py": "python",
      "ml": "machine learning",
      // ... 13 mappings total
    },
    "degree_map": {
      "btech": "B.Tech",
      "be": "B.E",
      // ... 14 mappings total
    },
    "city_map": {
      "bangalore": "Bangalore",
      "bengaluru": "Bangalore",
      // ... 15 mappings total
    },
    "company_suffixes": [
      "PVT LTD", "LIMITED", "LTD", "INC", "CORP", "CORPORATION", "LLC"
    ]
  }
}
```

#### 5. Salary Parsing Patterns
```json
{
  "salary_parsing": {
    "patterns": [
      {
        "name": "lpa_range",
        "pattern": "(\\d+(?:\\.\\d+)?)\\s*(?:-|to)\\s*(\\d+(?:\\.\\d+)?)\\s*(?:lpa|lakhs?\\s+per\\s+annum)",
        "confidence": 0.9
      },
      // ... 5 patterns total
    ],
    "default_currency": "INR",
    "default_period": "annual"
  }
}
```

## How It Works

### Incremental Processing Flow

#### First Run (All Emails)
```
1. Load all emails from Phase 2 (e.g., 1000 emails)
2. Process all 1000 emails (~8 minutes)
3. Extract structured job postings
4. Save results to CSV/JSON
5. Save processed email IDs to state file
```

#### Subsequent Runs (Only New Emails)
```
1. Load state file (1000 processed IDs)
2. Load all emails from Phase 2 (e.g., 1050 emails)
3. Filter: 1050 - 1000 = 50 new emails
4. Process only 50 new emails (~30 seconds)
5. Load existing results (1000 jobs)
6. Merge: 1000 + new jobs
7. Save updated results
8. Update state file (1050 IDs)
```

### Performance Comparison

| Run | Total Emails | New Emails | Processing Time | Speed Improvement |
|-----|--------------|------------|-----------------|-------------------|
| 1st | 1000 | 1000 | 8 minutes | - |
| 2nd | 1050 | 50 | 30 seconds | **90% faster** |
| 3rd | 1100 | 50 | 30 seconds | **90% faster** |

### Checkpoint System

The pipeline automatically saves checkpoints:
- **Frequency**: Every 50 emails (configurable)
- **Purpose**: Crash recovery
- **Behavior**: If crash occurs, restart notebook - it resumes from last checkpoint
- **No Duplicates**: State tracking prevents reprocessing

## Output Schema

### CSV Format (30 Columns)

| Column | Description | Example |
|--------|-------------|---------|
| `job_id` | Unique job identifier | `EMAIL123_JOB_1` |
| `email_id` | Source email ID | `EMAIL123` |
| `company_name` | Company name | `Tech Corp` |
| `company_canonical` | Normalized company name | `TECH` |
| `company_confidence` | Extraction confidence | `0.85` |
| `position_title` | Job title | `Software Engineer` |
| `position_level` | Seniority level | `Mid` |
| `position_confidence` | Extraction confidence | `0.85` |
| `skills_required` | Comma-separated skills | `Python, Javascript, React` |
| `skills_count` | Number of skills | `3` |
| `education_required` | Required degrees | `B.TECH, B.E` |
| `experience_min_years` | Minimum experience | `2` |
| `experience_max_years` | Maximum experience | `5` |
| `experience_type` | Experience category | `Mid Level` |
| `location_city` | City | `Bangalore` |
| `location_state` | State | `Karnataka` |
| `work_mode` | Work mode | `Remote` |
| `location_confidence` | Extraction confidence | `0.8` |
| `salary_min` | Minimum salary (INR) | `800000` |
| `salary_max` | Maximum salary (INR) | `1200000` |
| `salary_currency` | Currency | `INR` |
| `salary_period` | Period | `annual` |
| `salary_raw_text` | Original text | `8-12 lpa` |
| `salary_confidence` | Extraction confidence | `0.9` |
| `application_deadline` | Deadline date | `2025-12-31` |
| `apply_link` | Application URL | `https://...` |
| `contact_email` | Contact email | `hr@company.com` |
| `completeness_score` | Data completeness (0-1) | `0.75` |
| `extraction_timestamp` | Processing time | `2025-12-17T23:18:16` |
| `source_subject` | Email subject | `Job Opening - SE` |

### JSON Format

```json
{
  "job_id": "EMAIL123_JOB_1",
  "email_id": "EMAIL123",
  "company": {
    "name": "Tech Corp",
    "canonical_name": "TECH",
    "confidence": 0.85
  },
  "position": {
    "title": "Software Engineer",
    "level": "Mid",
    "confidence": 0.85
  },
  "requirements": {
    "skills": ["python", "javascript", "react"],
    "education": ["B.TECH", "B.E"],
    "experience_min": 2,
    "experience_max": 5,
    "experience_type": "Mid Level"
  },
  "location": {
    "city": "Bangalore",
    "state": "Karnataka",
    "work_mode": "Remote",
    "confidence": 0.8
  },
  "compensation": {
    "salary_min": 800000,
    "salary_max": 1200000,
    "currency": "INR",
    "period": "annual",
    "raw_text": "8-12 lpa",
    "confidence": 0.9
  },
  "application": {
    "deadline": "2025-12-31",
    "apply_link": null,
    "contact_email": "hr@company.com"
  },
  "metadata": {
    "completeness_score": 0.75,
    "extraction_timestamp": "2025-12-17T23:18:16.261894",
    "source_subject": "Job Opening - Software Engineer"
  }
}
```

## Customization Examples

### Add New Skill Mapping
```json
{
  "normalization": {
    "skill_map": {
      "vue": "vue.js",
      "angular": "angularjs",
      "docker": "docker"
    }
  }
}
```

### Add New City Mapping
```json
{
  "normalization": {
    "city_map": {
      "noida": "Noida",
      "greater noida": "Noida",
      "navi mumbai": "Mumbai"
    }
  }
}
```

### Add Custom Salary Pattern
```json
{
  "salary_parsing": {
    "patterns": [
      {
        "name": "usd_range",
        "pattern": "\\$(\\d+)k?\\s*-\\s*\\$(\\d+)k?",
        "confidence": 0.9
      }
    ]
  }
}
```

### Change Processing Limits
```json
{
  "processing": {
    "max_jobs_per_email": 10,
    "max_companies_per_email": 5,
    "max_positions_per_email": 5,
    "min_completeness_score": 0.5
  }
}
```

## Force Full Reprocessing

### Method 1: Edit Configuration
```json
{
  "incremental_processing": {
    "force_full_reprocess": true
  }
}
```

### Method 2: Delete State File
```bash
# Windows
del state\processed_message_ids.txt

# Linux/Mac
rm state/processed_message_ids.txt
```

## Analytics Report

The pipeline automatically generates analytics:

### Basic Statistics
- Total job postings
- Unique companies
- Unique positions
- Unique locations

### Top 10 Reports
- Top 10 hiring companies
- Top 10 job positions
- Top 10 locations

### Salary Statistics
- Jobs with salary information (%)
- Average salary (LPA)
- Median salary (LPA)

### Data Quality
- Average completeness score
- High/Medium/Low quality distribution

## Troubleshooting

### "No new emails to process"
**Cause**: All emails have been processed  
**Solution**:
- Check `state/processed_message_ids.txt` to see processed IDs
- Set `force_full_reprocess: true` in config to reprocess all
- Or delete the state file

### Configuration validation errors
**Cause**: Invalid or missing configuration fields  
**Solution**:
- Check `config.json` syntax (valid JSON)
- Ensure all required fields are present
- Compare with `config.example.json` if available

### Missing input file
**Cause**: Phase 2 output not found  
**Solution**:
- Ensure Phase 2 has been run successfully
- Check `input_file` path in config (relative to Phase 3 directory)
- Verify file exists: `../Phase 2/relevant_placement_emails.csv`

### Unicode encoding errors in logs
**Cause**: Windows console encoding issues with special characters (₹, 🏗️)  
**Impact**: Only affects console logging, not file output  
**Solution**: These are warnings only - pipeline works correctly

### Low completeness scores
**Cause**: Missing data in source emails  
**Solution**:
- Check `min_completeness_score` setting (default: 0.3)
- Lower threshold to include more jobs
- Review source emails for data quality

## What's New

### ✅ Refactoring Improvements
1. **Single Notebook Architecture** - All code in `entity_structuring.ipynb`
2. **Configuration File** - All hardcoded values moved to `config.json`
3. **Incremental Processing** - Only processes new emails
4. **State Management** - Tracks processed emails
5. **Checkpoint System** - Crash recovery support
6. **Comprehensive Validation** - Config validated on load
7. **Rich Normalization** - 13 skills, 14 degrees, 15 cities
8. **Advanced Parsing** - 5 salary patterns, 3 experience patterns

### 🎯 Benefits
- **90% faster** on subsequent runs
- **Easy customization** via config file
- **No code changes** needed for adjustments
- **Crash recovery** with checkpoints
- **No duplicates** with state tracking
- **Clean structure** with single notebook
- **Production ready** with comprehensive error handling
