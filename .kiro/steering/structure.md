# Project Structure

## Root Organization

```
placement-mail-analysis-system/
├── .git/                    # Version control
├── .kiro/                   # Kiro AI assistant configuration
│   └── steering/            # AI guidance documents
├── .venv/                   # Virtual environment (not committed)
├── phases/                  # Multi-phase pipeline implementation
│   ├── Phase 1/             # Email extraction from Gmail
│   ├── Phase 2/             # Data cleaning and filtering
│   ├── Phase 3/             # Entity extraction and structuring
│   ├── Phase 4/             # Job prioritization and ranking
│   ├── Phase 5/             # RAG system and conversational agent
│   └── Phase 6/             # Excel report generation
├── main.py                  # Application entry point
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Locked dependency versions
├── .python-version          # Python version specification
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

## Phase Organization

Each phase contains:
- **Jupyter notebooks** (`.ipynb`) - Interactive development and analysis
- **Data outputs** (`.csv`, `.json`) - Processed data from each phase
- **Log files** (`.log`) - Execution logs for debugging
- **Phase-specific folders** - attachments, state, vector_db, excel_reports

### Phase Pipeline Flow

1. **Phase 1**: Extract emails from Gmail API → `placement_emails.csv`
2. **Phase 2**: Clean and filter relevant emails → `relevant_placement_emails.csv`
3. **Phase 3**: Structure job postings with NLP → `structured_job_postings.json`
4. **Phase 4**: Prioritize and rank jobs → `prioritized_jobs.csv`
5. **Phase 5**: Build RAG system for Q&A → Vector database + conversational agent
6. **Phase 6**: Generate Excel reports → Formatted job tracking spreadsheets

## Code Organization Conventions

### File Naming
- Use lowercase with underscores for Python modules: `email_processor.py`
- Use descriptive names that reflect module purpose
- Jupyter notebooks use descriptive names: `data_extracting.ipynb`

### Notebook Structure
- Each phase has dedicated notebooks for specific tasks
- Notebooks should be self-contained but can reference previous phase outputs
- Keep notebooks focused on single responsibilities

### Data Flow
- Each phase reads from previous phase outputs
- Intermediate data stored in phase folders
- Final outputs can be aggregated in root `data/` folder (if created)

### Import Conventions
- Standard library imports first
- Third-party imports second
- Local application imports last
- Use absolute imports from project root

### Testing
- Place tests in `tests/` directory
- Name test files with `test_` prefix
- Use pytest fixtures for common setup
- Keep test data separate from production data

## Security & Sensitive Files

**NEVER commit these files:**
- `credentials.json` - Gmail API credentials
- `token.json` - OAuth tokens
- `config.json` - API keys and configuration
- Email attachments (may contain personal data)
- CSV files with actual email content
- Vector databases (may contain indexed personal data)

## Ignored Files

The following are excluded from version control:
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments (`.venv/`)
- Environment variables (`.env`)
- Credentials and tokens (`credentials.json`, `token.json`)
- Data outputs (`*.csv`, `*.json` in phases/)
- Attachments and state folders
- Vector databases
- Excel reports
- Build artifacts (`build/`, `dist/`, `*.egg-info`)
- IDE configurations (`.vscode/`, `.idea/`)
- Logs and coverage reports
- Jupyter checkpoints (`.ipynb_checkpoints/`)
- Temporary Excel files (`~$*.xlsx`)
