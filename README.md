# 📧 Placement Mail Analysis System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/AI-Google%20Gemini-orange.svg" alt="Gemini">
  <img src="https://img.shields.io/badge/Framework-FastAPI-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

<p align="center">
  <b>An AI-powered system for extracting, analyzing, and prioritizing job opportunities from placement emails</b>
</p>

---

## 🎯 Problem Statement

College students receive hundreds of placement emails containing job opportunities, but:
- Emails are unstructured and hard to track
- Important deadlines get missed
- No easy way to compare opportunities
- Manual tracking in spreadsheets is tedious

**This project solves these problems using AI and automation.**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📧 **Email Extraction** | Automatically fetch placement emails from Gmail |
| 🧹 **AI Cleaning** | Filter spam and extract relevant job postings |
| 🏢 **Entity Extraction** | Extract company, role, salary, skills using NLP |
| 📊 **Smart Ranking** | Prioritize jobs based on your preferences |
| 💬 **AI Chat Assistant** | Ask questions about jobs in natural language |
| 📈 **Excel Reports** | Generate professional tracking spreadsheets |
| 🌐 **Web Interface** | Modern chat UI for interacting with the system |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PLACEMENT MAIL ANALYSIS SYSTEM                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Phase 1  │───▶│ Phase 2  │───▶│ Phase 3  │───▶│ Phase 4  │  │
│  │  Gmail   │    │ Cleaning │    │   NLP    │    │ Ranking  │  │
│  │   API    │    │    AI    │    │ Extract  │    │  Score   │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                         │              │        │
│                                         ▼              ▼        │
│                                  ┌──────────┐   ┌──────────┐   │
│                                  │ Phase 5  │   │ Phase 6  │   │
│                                  │   RAG    │   │  Excel   │   │
│                                  │ ChatBot  │   │ Reports  │   │
│                                  └──────────┘   └──────────┘   │
│                                         │                       │
│                                         ▼                       │
│                                  ┌──────────┐                   │
│                                  │   Web    │                   │
│                                  │Interface │                   │
│                                  └──────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### AI & Machine Learning
- **Google Gemini** - LLM for text analysis and chat
- **Sentence Transformers** - Text embeddings
- **spaCy** - Named Entity Recognition
- **NLTK** - Text preprocessing

### Data & Storage
- **pandas** - Data manipulation
- **ChromaDB** - Vector database for RAG
- **SQLite** - Metadata storage

### Web & APIs
- **FastAPI** - Backend API server
- **Gmail API** - Email extraction
- **OAuth 2.0** - Authentication

### Document Processing
- **pdfplumber** - PDF text extraction
- **openpyxl** - Excel generation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Gmail account
- [Google Gemini API key](https://aistudio.google.com/apikey) (free)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/placement-mail-analysis-system.git
cd placement-mail-analysis-system

# Install uv package manager (if not installed)
pip install uv

# Install dependencies
uv sync

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Setup environment
python setup_env.py
```

### Configuration

1. **Environment Variables Setup**:
   ```bash
   # Copy example environment file
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```

2. **Get Gemini API Key** (Free):
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Create API key
   - Add to `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Phase 1 Configuration** (for email extraction):
   ```bash
   # Copy example config
   cd "phases/Phase 1"
   copy config.example.json config.json  # Windows
   cp config.example.json config.json    # Linux/Mac
   ```
   
   Edit `config.json` with your university's placement email address:
   ```json
   {
     "gmail_query": "from:placementoffice@youruniversity.edu OR subject:(Placement OR Internship)",
     ...
   }
   ```

4. **Gmail API Setup** (for email extraction):
   - Create [Google Cloud Project](https://console.cloud.google.com/)
   - Enable Gmail API
   - Download `credentials.json` to `phases/Phase 1/`

📖 **Detailed Setup:** Each phase has its own `README.md` with specific instructions

### Run Web Interface

```bash
python run_web.py
# Open http://localhost:8000
```

---

## 📁 Project Structure

```
placement-mail-analysis-system/
├── phases/                      # Six-phase pipeline
│   ├── Phase 1/                 # 📧 Email extraction
│   │   ├── README.md            # Phase 1 setup guide
│   │   ├── config.example.json  # Configuration template
│   │   └── data_extracting.ipynb
│   ├── Phase 2/                 # 🧹 Data cleaning
│   │   ├── README.md            # Phase 2 setup guide
│   │   └── *.ipynb
│   ├── Phase 3/                 # 🏢 Entity extraction
│   │   ├── README.md            # Phase 3 setup guide
│   │   └── entity_structuring.ipynb
│   ├── Phase 4/                 # 📊 Job prioritization
│   │   ├── README.md            # Phase 4 setup guide
│   │   └── job_prioritization.ipynb
│   ├── Phase 5/                 # 💬 RAG chatbot
│   │   ├── README.md            # Phase 5 setup guide
│   │   └── *.ipynb
│   └── Phase 6/                 # 📈 Excel reports
│       ├── README.md            # Phase 6 setup guide
│       └── Excel_Integrate.ipynb
├── web/                         # 🌐 Web interface
│   ├── app.py                   # FastAPI backend
│   └── templates/               # HTML templates
├── .env.example                 # Environment variables template
├── run_web.py                   # Start web server
├── run_pipeline.py              # Run data pipeline
├── setup_env.py                 # Setup helper
├── pyproject.toml               # Dependencies
└── README.md                    # Documentation
```

💡 **Tip:** Each phase folder contains a detailed `README.md` with setup instructions, dependencies, and troubleshooting guides.

---

## 💬 Usage Examples

### Chat with AI Assistant

```
You: "Show me Python developer jobs"
AI: "I found 5 Python developer positions:
     1. TCS - Python Developer (Bangalore, 8 LPA)
     2. Infosys - Backend Engineer (Hyderabad, 10 LPA)
     ..."

You: "Which jobs have the highest salary?"
AI: "The top paying positions are..."

You: "Remote work opportunities"
AI: "Here are remote-friendly positions..."
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Chat interface |
| `/api/chat` | POST | Send message to AI |
| `/api/jobs` | GET | Get job listings |
| `/api/stats` | GET | Get statistics |
| `/docs` | GET | API documentation |

---

## 📊 Sample Output

### Structured Job Data
```json
{
  "company": "Google",
  "position": "Software Engineer",
  "location": "Bangalore",
  "salary_range": "15-25 LPA",
  "skills": ["Python", "ML", "Cloud"],
  "deadline": "2025-01-15",
  "priority_score": 0.92
}
```

### Excel Report
- Dashboard with key metrics
- Top job recommendations
- Application tracker
- Skills gap analysis

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **API Integration** - Gmail API, OAuth 2.0
2. **NLP/NER** - Entity extraction with spaCy
3. **LLM Applications** - Gemini for text analysis
4. **RAG Systems** - Vector search with ChromaDB
5. **Web Development** - FastAPI + HTML/JS
6. **Data Engineering** - ETL pipeline design
7. **Python Best Practices** - Type hints, logging, error handling

---

## Cloud Deployment

### Deploy to Render (Free)

1. Fork this repository to your GitHub
2. Go to [render.com](https://render.com) and create account
3. Click "New" > "Web Service"
4. Connect your GitHub repo
5. Set environment variable: `GEMINI_API_KEY=your_key`
6. Deploy!

### Deploy to Railway (Free)

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

Set `GEMINI_API_KEY` in Railway dashboard.

### Deploy with Docker

```bash
docker build -t placement-assistant .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key placement-assistant
```

### Using Your Own Job Data

1. Export `prioritized_jobs.csv` from Phase 4
2. Place it in `data/jobs.csv`
3. Redeploy

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file.

---

## 👨‍💻 Author

**Vansh Bhardwaj**
- GitHub: [@vanshbhardwaj22](https://github.com/vanshbhardwaj22)
- LinkedIn: [Vansh Bhardwaj](https://www.linkedin.com/in/vanshbhardwaj2004)

---

## ⭐ Show Your Support

Give a ⭐ if this project helped you!

---

<p align="center">Made with ❤️ for placement season</p>
