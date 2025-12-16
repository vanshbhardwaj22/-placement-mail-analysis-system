import json

# Load the notebook
with open('phases/Phase 2/data_cleaning.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find the cell with KNOWLEDGE_BASE definition
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'KNOWLEDGE_BASE = {' in source and '# 3. ENHANCED KNOWLEDGE BASE' in source:
            print(f"Found KNOWLEDGE_BASE in cell {i}")
            
            # Replace the cell content
            new_source = '''# ===================================================================
# 3. LOAD CONFIGURATION
# ===================================================================

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"Configuration loaded from: {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        logger.error("Please create config.json with knowledge_base and patterns")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        return None

# Load configuration
CONFIG = load_config()

if CONFIG is None:
    logger.error("Cannot proceed without configuration!")
    raise SystemExit("Configuration file required")

# Extract knowledge base and patterns from config
KNOWLEDGE_BASE = {
    "skills": set(CONFIG.get("knowledge_base", {}).get("skills", [])),
    "positions": set(CONFIG.get("knowledge_base", {}).get("positions", [])),
    "locations": set(CONFIG.get("knowledge_base", {}).get("locations", [])),
    "degrees": set(CONFIG.get("knowledge_base", {}).get("degrees", []))
}

# Company patterns for regex
COMPANY_PATTERNS = CONFIG.get("extraction_patterns", {}).get("company_patterns", [])

# Salary patterns
SALARY_PATTERNS = CONFIG.get("extraction_patterns", {}).get("salary_patterns", [])

# Experience patterns
EXPERIENCE_PATTERNS = CONFIG.get("extraction_patterns", {}).get("experience_patterns", [])

logger.info(f"Loaded {len(KNOWLEDGE_BASE['skills'])} skills")
logger.info(f"Loaded {len(KNOWLEDGE_BASE['positions'])} positions")
logger.info(f"Loaded {len(KNOWLEDGE_BASE['locations'])} locations")
logger.info(f"Loaded {len(KNOWLEDGE_BASE['degrees'])} degrees")

# Text cleaning patterns from config
REMOVE_PATTERNS = CONFIG.get("text_cleaning", {}).get("remove_patterns", [])
'''
            
            # Split into lines for notebook format
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            # Remove trailing newline from last line
            if cell['source']:
                cell['source'][-1] = cell['source'][-1].rstrip('\n')
            
            print("Cell updated successfully")
            break

# Also update the REMOVE_PATTERNS section
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'REMOVE_PATTERNS = [' in source and '# Regex for cleaning' in source:
            print(f"Found REMOVE_PATTERNS in cell {i}")
            # This section is now loaded from config, so we can simplify it
            new_source = '''# ===================================================================
# 4. AGGRESSIVE TEXT CLEANING
# ===================================================================

# Regex for cleaning
URL_RE = re.compile(r'https?://\\S+|www\\.\\S+')
EMAIL_RE = re.compile(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b')
PHONE_RE = re.compile(r'[\\+]?[\\d][\\d\\s\\-\\(\\)]{7,}[\\d]')
HTML_RE = re.compile(r'<[^>]+>')
NON_PRINTABLE = re.compile(r'[^\\x20-\\x7E\\n\\r]+')

# REMOVE_PATTERNS loaded from config above
'''
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            if cell['source']:
                cell['source'][-1] = cell['source'][-1].rstrip('\n')
            print("REMOVE_PATTERNS cell updated")
            break

# Update the main pipeline to use config paths
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'if __name__ == "__main__":' in source and 'CSV_PATH = r"D:' in source:
            print(f"Found main execution in cell {i}")
            new_source = '''# ===================================================================
# 10. USAGE
# ===================================================================

if __name__ == "__main__":
    # Load paths from config
    CSV_PATH = CONFIG.get("input_csv", "../Phase 1/placement_emails.csv")
    OUTPUT_PATH = CONFIG.get("output_csv", "ai_cleaned_emails.csv")
    
    df = main_ai_pipeline(CSV_PATH, OUTPUT_PATH)
    
    if df is not None:
        logger.info("AI-powered pipeline complete!")
        logger.info(f"Check output: {OUTPUT_PATH}")
'''
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            if cell['source']:
                cell['source'][-1] = cell['source'][-1].rstrip('\n')
            print("Main execution cell updated")
            break

# Save the updated notebook
with open('phases/Phase 2/data_cleaning.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\nNotebook updated successfully!")
print("The notebook now loads configuration from config.json")
