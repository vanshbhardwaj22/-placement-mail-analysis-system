# Phase 3: Entity Extraction & Structuring

## Overview

Phase 3 extracts structured job information from cleaned emails using Natural Language Processing.

## Setup Instructions

### Required Inputs

- `../Phase 2/relevant_placement_emails.csv` - Filtered emails from Phase 2

### Dependencies

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install required packages
pip install pandas spacy nltk
python -m spacy download en_core_web_sm
```

## Component

### entity_structuring.ipynb

**Purpose:** Extract and structure job posting details using NER (Named Entity Recognition)

**Extracted Information:**
- Company name
- Job title/role
- Required skills and qualifications
- Location (city, state, country)
- Salary range
- Application deadline
- Contact information (email, phone)
- Job type (full-time, internship, etc.)
- Experience level required

**NLP Techniques:**
- Named Entity Recognition (NER) with spaCy
- Pattern matching for structured data
- Regex extraction for dates, emails, phones
- Skill keyword extraction
- Location normalization

## Running Phase 3

```bash
jupyter notebook entity_structuring.ipynb
```

## Outputs

- `structured_job_postings.json` - Structured job data (JSON format)
- `structured_job_postings.csv` - Structured job data (tabular format)
- `entity_structuring.log` - Processing logs and errors

## Data Structure

Each job posting contains:

```json
{
  "job_id": "unique_identifier",
  "company": "Company Name",
  "role": "Job Title",
  "skills": ["Python", "Machine Learning", "SQL"],
  "location": {
    "city": "City",
    "state": "State",
    "country": "Country",
    "remote": true/false
  },
  "salary": {
    "min": 50000,
    "max": 80000,
    "currency": "USD"
  },
  "deadline": "2024-12-31",
  "contact": {
    "email": "hr@company.com",
    "phone": "+1-234-567-8900"
  },
  "job_type": "Full-time",
  "experience_level": "Entry Level",
  "description": "Full job description text",
  "source_email_id": "original_email_id"
}
```

## Quality Metrics

The notebook tracks:
- Number of jobs extracted
- Extraction success rate per field
- Missing data percentage
- Entity recognition accuracy

## Troubleshooting

### Low Extraction Accuracy

If many fields are missing:
- Check email format consistency
- Review extraction patterns in notebook
- Adjust NER confidence thresholds
- Add custom entity patterns

### spaCy Model Issues

```
Error: Can't find model 'en_core_web_sm'
```
**Solution:**
```bash
python -m spacy download en_core_web_sm
```

For better accuracy, use larger model:
```bash
python -m spacy download en_core_web_md
# Update notebook to use 'en_core_web_md'
```

### Date Parsing Errors

If deadline extraction fails:
- Check date format variations in emails
- Add custom date patterns
- Review `entity_structuring.log` for patterns

### Memory Issues

For large datasets:
- Process emails in batches
- Reduce spaCy pipeline components
- Use smaller spaCy model
