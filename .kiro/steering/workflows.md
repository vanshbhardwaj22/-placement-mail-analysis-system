# Workflow Guide

## Six-Phase Pipeline Architecture

This project implements a sequential pipeline for processing placement emails into actionable job insights.

## Phase Execution Order

### Phase 1: Email Extraction
**Notebook**: `phases/Phase 1/data_extracting.ipynb`

**Purpose**: Connect to Gmail API and extract placement-related emails

**Inputs**:
- `credentials.json` - Gmail API credentials
- Gmail account with placement emails

**Outputs**:
- `placement_emails.csv` - Raw email data
- `token.json` - OAuth token for future access
- `attachments/` - Downloaded email attachments

**Key Operations**:
- Gmail API authentication
- Email query and filtering
- Attachment downloading
- CSV export

---

### Phase 2: Data Cleaning & Filtering
**Notebooks**: 
- `phases/Phase 2/data_cleaning.ipynb`
- `phases/Phase 2/data_filtering.ipynb`

**Purpose**: Clean email text and filter relevant placement opportunities

**Inputs**:
- `placement_emails.csv` from Phase 1

**Outputs**:
- `ai_cleaned_emails.csv` - Cleaned email content
- `relevant_placement_emails.csv` - Filtered relevant emails

**Key Operations**:
- Text normalization and cleaning
- Spam/irrelevant email filtering
- AI-powered relevance classification
- Data quality validation

---

### Phase 3: Entity Extraction & Structuring
**Notebook**: `phases/Phase 3/entity_structuring.ipynb`

**Purpose**: Extract structured job information using NLP

**Inputs**:
- `relevant_placement_emails.csv` from Phase 2

**Outputs**:
- `structured_job_postings.json` - Structured job data
- `structured_job_postings.csv` - Tabular format
- `entity_structuring.log` - Processing logs

**Key Operations**:
- Named Entity Recognition (NER) with spaCy
- Job detail extraction (company, role, requirements, etc.)
- Data structuring and normalization
- JSON/CSV export

**Extracted Fields**:
- Company name
- Job title/role
- Required skills
- Location
- Salary range
- Application deadline
- Contact information

---

### Phase 4: Job Prioritization
**Notebook**: `phases/Phase 4/job_prioritization.ipynb`

**Purpose**: Rank and prioritize jobs based on relevance and fit

**Inputs**:
- `structured_job_postings.json` from Phase 3

**Outputs**:
- `prioritized_jobs.csv` - All jobs with priority scores
- `top_recommendations.csv` - Top-ranked opportunities
- `job_prioritization.log` - Scoring logs

**Key Operations**:
- Feature engineering (skills match, location preference, etc.)
- Scoring algorithm application
- Ranking and sorting
- Top N recommendations

**Scoring Criteria**:
- Skills alignment
- Company reputation
- Compensation
- Location preference
- Application deadline urgency

---

### Phase 5: RAG System & Conversational Agent
**Notebooks**:
- `phases/Phase 5/PDF_Management.ipynb`
- `phases/Phase 5/RAG_System.ipynb`
- `phases/Phase 5/Conversational_agent.ipynb`

**Purpose**: Build intelligent Q&A system for job search queries

**Inputs**:
- `structured_job_postings.json` from Phase 3
- PDF documents (resumes, job descriptions)

**Outputs**:
- `vector_db/` - ChromaDB vector database
- `pdf_metadata.json` - PDF indexing metadata
- Log files for each component

**Key Operations**:
- PDF text extraction and chunking
- Vector embedding generation (Sentence Transformers)
- ChromaDB indexing
- RAG-based question answering
- Conversational interface with Gemini

**Use Cases**:
- "What jobs match my Python skills?"
- "Show me remote opportunities"
- "Which companies are hiring for data science?"
- "What are the salary ranges for ML roles?"

---

### Phase 6: Excel Report Generation
**Notebook**: `phases/Phase 6/Excel_Integrate.ipynb`

**Purpose**: Generate formatted Excel reports for job tracking

**Inputs**:
- `prioritized_jobs.csv` from Phase 4
- `structured_job_postings.json` from Phase 3

**Outputs**:
- `excel_reports/job_search_report_YYYYMMDD.xlsx` - Formatted report
- `excel_reports/application_tracker.xlsx` - Application tracking sheet
- `excel_automation.log` - Generation logs

**Key Operations**:
- Excel workbook creation
- Data formatting and styling
- Chart generation
- Conditional formatting
- Multi-sheet organization

**Report Sections**:
- Dashboard summary
- Top recommendations
- All opportunities (filterable)
- Application tracker
- Skills gap analysis

---

## Running the Pipeline

### Sequential Execution (Recommended)
```bash
# Activate environment
.venv\Scripts\activate

# Run each phase in order
jupyter notebook "phases/Phase 1/data_extracting.ipynb"
# ... complete Phase 1, then move to Phase 2
jupyter notebook "phases/Phase 2/data_cleaning.ipynb"
# ... and so on
```

### Individual Phase Execution
Each phase can be run independently if you have the required input files from previous phases.

### Automation (Future)
Consider creating a `main.py` orchestrator that runs all phases sequentially with error handling.

---

## Best Practices

1. **Always run phases in order** - Each phase depends on previous outputs
2. **Check logs** - Review `.log` files if issues occur
3. **Backup credentials** - Keep `credentials.json` secure and backed up separately
4. **Monitor API quotas** - Gmail API has daily limits
5. **Version control notebooks** - Commit notebook changes but not outputs
6. **Clean old data** - Periodically archive old CSV/JSON files
7. **Test with small datasets** - Use email filters to test with limited data first

---

## Troubleshooting

### Phase 1 Issues
- **Authentication errors**: Delete `token.json` and re-authenticate
- **No emails found**: Check Gmail query filters
- **API quota exceeded**: Wait 24 hours or request quota increase

### Phase 2-3 Issues
- **AI API errors**: Check API keys in environment variables
- **NLP model errors**: Ensure spaCy models are downloaded (`python -m spacy download en_core_web_sm`)

### Phase 5 Issues
- **ChromaDB errors**: Delete `vector_db/` folder and rebuild
- **Embedding errors**: Check sentence-transformers model download

### Phase 6 Issues
- **Excel file locked**: Close any open Excel files
- **Formatting errors**: Check openpyxl/xlsxwriter versions
