# Phase 1: Email Extraction

## Setup Instructions

### 1. Configuration File Setup

Before running Phase 1, you need to create your own `config.json` file:

```bash
# Copy the example configuration
cp config.example.json config.json
```

Then edit `config.json` with your specific settings:

#### Required Configuration Fields

- **gmail_query**: Gmail search query to filter placement emails
  - Example: `"from:placementoffice@youruniversity.edu OR subject:(Placement OR Internship OR Hiring)"`
  - Customize with your placement office email address

- **output_csv**: Output filename for extracted emails
  - Default: `"placement_emails.csv"`

- **api_scopes**: Gmail API permissions (usually no change needed)
  - Default: `["https://www.googleapis.com/auth/gmail.readonly"]`

- **credentials_file**: Path to Gmail API credentials
  - Default: `"credentials.json"`
  - See "Gmail API Setup" section below

- **token_file**: Path to store OAuth token
  - Default: `"token.json"`

#### Filter Configuration

Customize the filters section to match your needs:

- **allowed_sender_domains**: Email domains to accept
  - Add your university domain (e.g., `"youruniversity.edu"`)
  - Add common placement-related keywords

- **spam_subject_keywords**: Keywords to filter out spam
  - Add terms that appear in non-placement emails

- **required_placement_terms**: Keywords that indicate placement emails
  - Add terms specific to your placement process

### 2. Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download credentials and save as `credentials.json` in this folder

### 3. Running Phase 1

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Run the notebook
jupyter notebook data_extracting.ipynb
```

On first run, you'll be prompted to authenticate with Google. This creates `token.json` for future use.

## Outputs

- `placement_emails.csv` - Extracted email data
- `token.json` - OAuth authentication token
- `attachments/` - Downloaded email attachments

## Security Notes

⚠️ **NEVER commit these files to GitHub:**
- `config.json` - Contains your specific email addresses
- `credentials.json` - Contains API credentials
- `token.json` - Contains authentication tokens
- `*.csv` files - May contain personal/sensitive data
- `attachments/` folder - May contain sensitive documents

