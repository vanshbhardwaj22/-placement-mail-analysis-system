# Phase 5: RAG System & Conversational Agent

## Setup Instructions

### 1. Environment Variables Setup

Phase 5 requires a Gemini API key for AI-powered features. Set it up using the `.env` file:

```bash
# From project root, copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Then edit `.env` and add your Gemini API key:

```bash
GEMINI_API_KEY=your_actual_api_key_here
```

#### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

### 2. Required Inputs

Phase 5 depends on outputs from previous phases:

- `../Phase 3/structured_job_postings.json` - Structured job data
- `../Phase 4/prioritized_jobs.csv` - Prioritized job listings
- PDF files in `./pdfs/` directory (optional, for document Q&A)

### 3. Components

Phase 5 consists of three notebooks:

#### a) PDF_Management.ipynb
- Extracts text from PDF documents
- Generates AI summaries using Gemini
- Creates metadata for document indexing

**Usage:**
```python
from PDF_Management import PDFManager

pdf_manager = PDFManager(
    pdf_directory="./pdfs",
    gemini_api_key=os.getenv('GEMINI_API_KEY')
)

# Process all PDFs
pdf_manager.process_all_pdfs()
```

#### b) RAG_System.ipynb
- Builds vector database using ChromaDB
- Creates embeddings with Sentence Transformers
- Enables semantic search over job postings

**Usage:**
```python
from RAG_System import RAGSystem

rag = RAGSystem()
rag.index_documents(structured_jobs)

# Search for relevant jobs
results = rag.search("Python developer remote")
```

#### c) Conversational_agent.ipynb
- Interactive Q&A interface
- Natural language queries about jobs
- Context-aware responses using RAG + Gemini

**Usage:**
```python
from Conversational_agent import ConversationalAgent

agent = ConversationalAgent(
    gemini_api_key=os.getenv('GEMINI_API_KEY'),
    jobs_csv_path="../Phase 4/prioritized_jobs.csv"
)

# Ask questions
response = agent.chat("What are the best Python jobs for me?")
```

### 4. Running Phase 5

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install required packages (if not already installed)
pip install google-generativeai sentence-transformers chromadb

# Run notebooks in order
jupyter notebook PDF_Management.ipynb
jupyter notebook RAG_System.ipynb
jupyter notebook Conversational_agent.ipynb
```

## Outputs

- `vector_db/` - ChromaDB vector database
- `pdf_metadata.json` - PDF indexing metadata
- `pdf_manager.log` - PDF processing logs
- `rag_system.log` - RAG system logs
- `conversational_agent.log` - Agent interaction logs

## Example Queries

Once the conversational agent is running, you can ask:

- "What jobs match my Python and machine learning skills?"
- "Show me remote opportunities with good salary"
- "Which companies are hiring for data science roles?"
- "What are the requirements for the Google position?"
- "Find jobs with application deadlines this week"

## Security Notes

⚠️ **NEVER commit these files to GitHub:**
- `.env` - Contains your API keys
- `pdf_metadata.json` - May contain sensitive document info
- `vector_db/` - Contains indexed data
- `*.log` files - May contain query history

These files are already listed in `.gitignore` for your protection.

## Troubleshooting

### API Key Issues
```
Error: GEMINI_API_KEY not found
```
**Solution:** Ensure `.env` file exists in project root with valid API key

### ChromaDB Issues
```
Error: ChromaDB connection failed
```
**Solution:** Delete `vector_db/` folder and rebuild:
```bash
rm -rf vector_db  # Linux/Mac
rmdir /s vector_db  # Windows
```

### Embedding Model Issues
```
Error: sentence-transformers model not found
```
**Solution:** First run will download the model automatically. Ensure internet connection.

### Memory Issues
If processing large PDFs or many documents:
- Process PDFs in smaller batches
- Reduce chunk size in RAG configuration
- Increase system RAM allocation
