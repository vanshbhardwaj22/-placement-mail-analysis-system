# Phase 2: Data Cleaning & Filtering

## Overview

Phase 2 processes raw email data from Phase 1 to clean and filter relevant placement opportunities using AI-powered NLP and a configuration-driven approach.

## Config Integration

The `data_cleaning.ipynb` notebook is now fully integrated with `config.json`, providing a flexible and maintainable approach to data processing.

### Key Features

1. **Configuration-Driven**: All settings loaded from `config.json`
   - Knowledge base (skills, positions, locations, degrees)
   - Extraction patterns (company, salary, experience)
   - Text cleaning rules
   - File paths

2. **Dynamic Knowledge Base**
   - Skills: Programming languages, frameworks, tools
   - Positions: Job titles and roles
   - Locations: Cities and remote options
   - Degrees: Educational qualifications

3. **Easy Customization**
   - Update patterns without modifying code
   - Add new skills, positions, or patterns by editing JSON
   - Share configurations across team members

### Benefits

- **Maintainability**: Update patterns and knowledge base without modifying code
- **Flexibility**: Easy to customize for different use cases
- **Scalability**: Add new skills, positions, or patterns by editing JSON
- **Portability**: Share configurations across team members
- **Version Control**: Track configuration changes separately from code

## Setup Instructions

### 1. Configuration File Setup

Before running Phase 2, create your own `config.json` file:

```bash
# Copy the example configuration
copy config.example.json config.json  # Windows
cp config.example.json config.json    # Linux/Mac
```

The `config.json` file contains:
- **Knowledge Base**: Skills, positions, locations, and degrees to extract
- **Extraction Patterns**: Regex patterns for companies, salaries, and experience
- **Text Cleaning Rules**: Patterns to remove from emails
- **Processing Settings**: Batch size and text limits

You can customize the knowledge base to match your specific needs (e.g., add new skills, locations, or job titles).

### 2. Required Inputs

- `../Phase 1/placement_emails.csv` - Raw email data from Phase 1

### 3. Dependencies

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install required packages
pip install pandas numpy spacy nltk
python -m spacy download en_core_web_sm
```

## Components

### 1. data_cleaning.ipynb

**Purpose:** Clean and normalize email text using AI-powered NLP

**Operations:**
- Remove HTML tags and formatting
- Normalize whitespace and encoding
- Extract clean text content
- Remove duplicates
- Handle special characters

**Output:** `ai_cleaned_emails.csv`

### 2. data_filtering.ipynb

**Purpose:** Filter relevant placement emails from cleaned data

**Operations:**
- Spam detection and removal
- Relevance classification
- Keyword-based filtering
- Domain validation
- Quality scoring

**Output:** `relevant_placement_emails.csv`

## Running Phase 2

The `data_cleaning.ipynb` notebook now automatically loads configuration from `config.json`.

```bash
# Run notebooks in order
jupyter notebook data_cleaning.ipynb
jupyter notebook data_filtering.ipynb
```

The notebook will:
1. Load configuration from `config.json`
2. Extract knowledge base (skills, positions, locations, degrees)
3. Load extraction patterns (company, salary, experience)
4. Apply text cleaning rules
5. Process emails and extract entities

### Usage Options

**Option 1: Use Config Defaults**
```python
# Simply run the pipeline - uses config.json settings
df = main_ai_pipeline()
```

**Option 2: Override Config**
```python
# Override specific paths if needed
df = main_ai_pipeline(
    csv_path='custom_input.csv',
    output_path='custom_output.csv'
)
```

## Outputs

- `ai_cleaned_emails.csv` - Cleaned email content
- `relevant_placement_emails.csv` - Filtered relevant emails

## Configuration

### Knowledge Base Customization

Edit `config.json` to customize what information gets extracted:

#### Adding New Skills
```json
"skills": [
  "python", "java", "javascript",
  "your-new-skill-here"
]
```

#### Adding New Locations
```json
"locations": [
  "bangalore", "mumbai", "delhi",
  "your-city-here"
]
```

#### Adding New Job Positions
```json
"positions": [
  "software engineer", "data scientist",
  "your-position-here"
]
```

#### Customizing Extraction Patterns

You can modify regex patterns for better extraction:

```json
"extraction_patterns": {
  "salary_patterns": [
    "(\\d+(?:\\.\\d+)?)\\s*(?:lpa|lakhs?\\s+per\\s+annum)",
    "your-custom-pattern-here"
  ]
}
```

### Text Cleaning Rules

Customize what gets removed from emails:

```json
"text_cleaning": {
  "remove_patterns": [
    "regards?,?.*",
    "your-pattern-here"
  ],
  "min_line_length": 5
}
```

## Quality Metrics

The notebooks track:
- Number of emails processed
- Cleaning success rate
- Spam detection accuracy
- Relevant email percentage

## Configuration Structure

```json
{
  "input_csv": "../Phase 1/placement_emails.csv",
  "output_csv": "ai_cleaned_emails.csv",
  "knowledge_base": {
    "skills": [...],
    "positions": [...],
    "locations": [...],
    "degrees": [...]
  },
  "extraction_patterns": {
    "company_patterns": [...],
    "salary_patterns": [...],
    "experience_patterns": [...]
  },
  "text_cleaning": {
    "remove_patterns": [...],
    "min_line_length": 5
  }
}
```

## Comparison: Before vs After Integration

| Feature | Before | After |
|---------|--------|-------|
| Knowledge Base | Hardcoded | Config-driven |
| Patterns | Hardcoded | Config-driven |
| File Paths | Hardcoded | Config-driven |
| Cleaning Rules | Hardcoded | Config-driven |
| Extensibility | Requires code changes | Edit JSON file |
| Team Sharing | Share notebook | Share config + notebook |

## Troubleshooting

### Config Not Found
```
Error: Config file not found: config.json
```
**Solution:**
```bash
copy config.example.json config.json  # Windows
cp config.example.json config.json    # Linux/Mac
```

### Invalid JSON
```
Error: Invalid JSON in config file
```
**Solution:** Validate JSON syntax using a JSON validator (e.g., jsonlint.com)

### spaCy Model Missing
```
Error: Can't find model 'en_core_web_sm'
```
**Solution:**
```bash
python -m spacy download en_core_web_sm  # Basic
python -m spacy download en_core_web_lg  # Better accuracy
python -m spacy download en_core_web_trf # Best accuracy
```

### Memory Issues
If processing large datasets:
- Process in smaller batches
- Increase chunk size parameter
- Close other applications

### Encoding Errors
```
Error: UnicodeDecodeError
```
**Solution:** The cleaning pipeline handles most encoding issues automatically. If persistent, check source CSV encoding.
