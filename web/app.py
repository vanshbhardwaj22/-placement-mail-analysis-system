"""
Placement Mail Analysis System - Web Interface
FastAPI backend for the conversational job search agent.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Google Generative AI
from google import genai
from google.genai import types

# Logging setup (cloud-friendly - no file handler)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("WebAgent")

# FastAPI app
app = FastAPI(
    title="Placement Job Search Assistant",
    description="AI-powered job search assistant for placement opportunities",
    version="1.0.0"
)

# Templates
templates = Jinja2Templates(directory="web/templates")


# ============================================================
# DATA MODELS
# ============================================================

class ChatMessage(BaseModel):
    message: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    status: str
    response: str
    intent: Optional[str] = None
    jobs: Optional[List[Dict]] = None
    timestamp: str


class QueryIntent(Enum):
    JOB_SEARCH = "job_search"
    JOB_DETAILS = "job_details"
    SKILL_ANALYSIS = "skill_analysis"
    COMPARE_JOBS = "compare_jobs"
    APPLICATION_HELP = "application_help"
    SALARY_INFO = "salary_info"
    LOCATION_QUERY = "location_query"
    COMPANY_INFO = "company_info"
    GENERAL_CHAT = "general_chat"
    UNKNOWN = "unknown"


@dataclass
class UserContext:
    user_id: str
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    
    def add_message(self, role: str, content: str):
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def get_context(self) -> str:
        return "\n".join([
            f"{m['role'].title()}: {m['content']}" 
            for m in self.conversation_history[-5:]
        ])


# ============================================================
# JOB SEARCH AGENT
# ============================================================

class JobSearchAgent:
    """Main agent for handling job search queries."""
    
    def __init__(self):
        self.logger = logging.getLogger("JobSearchAgent")
        self.user_contexts: Dict[str, UserContext] = {}
        
        # Initialize Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            self.logger.error("GEMINI_API_KEY not found!")
            raise ValueError("GEMINI_API_KEY environment variable required")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"
        self.logger.info("[OK] Gemini client initialized")
        
        # Load jobs data
        self.jobs_df = self._load_jobs()
        self.logger.info(f"[OK] Loaded {len(self.jobs_df)} jobs")
        
        # System prompt
        self.system_prompt = """You are an intelligent job search assistant for a placement system.

Your role:
- Help users find relevant job opportunities from placement emails
- Provide detailed job information when asked
- Analyze skills and requirements
- Give application advice
- Be friendly, professional, and helpful

When presenting jobs, format them clearly with:
- Company name and position
- Location and salary (if available)
- Key requirements

Keep responses concise but informative. Use bullet points for lists."""

    def _load_jobs(self) -> pd.DataFrame:
        """Load jobs from various possible locations."""
        paths = [
            # Cloud deployment paths
            "data/jobs.csv",
            "data/prioritized_jobs.csv",
            # Local development paths
            "phases/Phase 4/prioritized_jobs.csv",
            "../phases/Phase 4/prioritized_jobs.csv",
            # Environment variable path
            os.getenv("JOBS_CSV_PATH", ""),
        ]
        for path in paths:
            if path and os.path.exists(path):
                self.logger.info(f"Loading jobs from: {path}")
                return pd.read_csv(path)
        
        self.logger.warning("Jobs CSV not found, using sample data")
        # Return sample data for demo purposes
        return self._get_sample_jobs()
    
    def _get_sample_jobs(self) -> pd.DataFrame:
        """Return sample job data for demo when no CSV is available."""
        sample_data = [
            {
                "job_id": 1,
                "company_name": "TechCorp India",
                "position_title": "Software Developer",
                "location_city": "Bangalore",
                "salary_max": "12 LPA",
                "skills_required": "Python, JavaScript, React, SQL",
                "job_description": "Full stack development role"
            },
            {
                "job_id": 2,
                "company_name": "DataSoft Solutions",
                "position_title": "Data Analyst",
                "location_city": "Hyderabad",
                "salary_max": "8 LPA",
                "skills_required": "Python, SQL, Excel, Tableau",
                "job_description": "Business analytics and reporting"
            },
            {
                "job_id": 3,
                "company_name": "CloudNet Systems",
                "position_title": "DevOps Engineer",
                "location_city": "Pune",
                "salary_max": "15 LPA",
                "skills_required": "AWS, Docker, Kubernetes, CI/CD",
                "job_description": "Cloud infrastructure management"
            },
            {
                "job_id": 4,
                "company_name": "AI Innovations",
                "position_title": "ML Engineer",
                "location_city": "Bangalore",
                "salary_max": "18 LPA",
                "skills_required": "Python, TensorFlow, PyTorch, NLP",
                "job_description": "Machine learning model development"
            },
            {
                "job_id": 5,
                "company_name": "WebTech Global",
                "position_title": "Frontend Developer",
                "location_city": "Remote",
                "salary_max": "10 LPA",
                "skills_required": "React, TypeScript, CSS, HTML",
                "job_description": "UI/UX development for web apps"
            }
        ]
        return pd.DataFrame(sample_data)
    
    def get_context(self, user_id: str) -> UserContext:
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = UserContext(user_id=user_id)
        return self.user_contexts[user_id]
    
    def search_jobs(self, query: str) -> List[Dict]:
        """Search jobs based on query keywords."""
        if self.jobs_df.empty:
            return []
        
        query_lower = query.lower()
        keywords = query_lower.split()
        
        # Search across multiple columns
        search_cols = ['company_name', 'position_title', 'skills_required', 
                       'location_city', 'job_description']
        
        mask = pd.Series([False] * len(self.jobs_df))
        for col in search_cols:
            if col in self.jobs_df.columns:
                col_str = self.jobs_df[col].fillna('').astype(str).str.lower()
                for kw in keywords:
                    mask |= col_str.str.contains(kw, na=False)
        
        results = self.jobs_df[mask].head(5)
        
        # Convert to list of dicts with safe column access
        jobs = []
        for _, row in results.iterrows():
            job = {
                'company': row.get('company_name', 'N/A'),
                'position': row.get('position_title', 'N/A'),
                'location': row.get('location_city', 'N/A'),
                'salary': row.get('salary_max', 'N/A'),
                'skills': row.get('skills_required', 'N/A')[:100] if pd.notna(row.get('skills_required')) else 'N/A'
            }
            jobs.append(job)
        
        return jobs
    
    async def process_query(self, query: str, user_id: str) -> Dict[str, Any]:
        """Process user query and generate response."""
        context = self.get_context(user_id)
        context.add_message('user', query)
        
        try:
            # Search for relevant jobs
            jobs = self.search_jobs(query)
            
            # Build prompt with context and job data
            jobs_info = ""
            if jobs:
                jobs_info = "\n\nRelevant jobs found:\n"
                for i, job in enumerate(jobs, 1):
                    jobs_info += f"{i}. {job['company']} - {job['position']}\n"
                    jobs_info += f"   Location: {job['location']}, Salary: {job['salary']}\n"
                    jobs_info += f"   Skills: {job['skills']}\n"
            
            prompt = f"""Conversation context:
{context.get_context()}

User query: "{query}"
{jobs_info}

Provide a helpful response. If jobs were found, summarize them nicely.
If no jobs match, suggest broadening the search or ask clarifying questions."""

            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.7
                )
            )
            
            response_text = response.text.strip()
            context.add_message('assistant', response_text)
            
            return {
                'status': 'success',
                'response': response_text,
                'jobs': jobs,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return {
                'status': 'error',
                'response': f"Sorry, I encountered an error: {str(e)}",
                'jobs': [],
                'timestamp': datetime.now().isoformat()
            }


# Initialize agent
agent = None

@app.on_event("startup")
async def startup():
    global agent
    try:
        agent = JobSearchAgent()
        logger.info("[OK] Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")


# ============================================================
# API ROUTES
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the chat interface."""
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Process chat message and return response."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    result = await agent.process_query(message.message, message.user_id)
    
    return ChatResponse(
        status=result['status'],
        response=result['response'],
        jobs=result.get('jobs'),
        timestamp=result['timestamp']
    )


@app.get("/api/jobs")
async def get_jobs(limit: int = 10):
    """Get top prioritized jobs."""
    if not agent or agent.jobs_df.empty:
        return {"jobs": [], "total": 0}
    
    jobs = agent.jobs_df.head(limit).to_dict('records')
    return {"jobs": jobs, "total": len(agent.jobs_df)}


@app.get("/api/stats")
async def get_stats():
    """Get job statistics."""
    if not agent or agent.jobs_df.empty:
        return {"total_jobs": 0, "companies": 0, "locations": 0}
    
    df = agent.jobs_df
    return {
        "total_jobs": len(df),
        "companies": df['company_name'].nunique() if 'company_name' in df.columns else 0,
        "locations": df['location_city'].nunique() if 'location_city' in df.columns else 0
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "agent_ready": agent is not None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
