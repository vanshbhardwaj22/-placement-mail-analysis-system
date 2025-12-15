# Technology Stack

## Build System

- **Package Manager**: `uv` (modern Python package manager)
- **Python Version**: 3.12+
- **Project Config**: `pyproject.toml`

## Core Technologies

### AI & ML
- Google Generative AI (Gemini models)
- Sentence Transformers for embeddings
- spaCy for NLP
- NLTK for text processing

### Data Processing
- pandas for data manipulation
- ChromaDB for vector storage
- pdfplumber and PyPDF2 for PDF extraction

### APIs & Integration
- Google API Client (Gmail integration)
- OAuth 2.0 authentication
- REST APIs via requests

### Data Export
- openpyxl and xlsxwriter for Excel generation

### Development
- pytest for testing
- hypothesis for property-based testing
- python-dotenv for environment management

## Common Commands

### Environment Setup
```bash
# Install dependencies
uv sync

# Activate virtual environment
.venv\Scripts\activate  # Windows
```

### Running
```bash
# Run main application
python main.py

# Or with uv
uv run main.py
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov
```

### Development
```bash
# Add new dependency
uv add <package-name>

# Add dev dependency
uv add --dev <package-name>
```

## Environment Variables

Store sensitive credentials in `.env` file (never commit):
- Google API credentials
- OAuth tokens
- API keys for AI services
