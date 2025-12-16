# Phase 6: Excel Report Generation

## Overview

Phase 6 generates formatted Excel reports for job tracking and analysis.

## Setup Instructions

### Required Inputs

- `../Phase 4/prioritized_jobs.csv` - Prioritized job listings
- `../Phase 3/structured_job_postings.json` - Structured job data (optional)

### Dependencies

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install required packages
pip install pandas openpyxl xlsxwriter
```

## Component

### Excel_Integrate.ipynb

**Purpose:** Create professional Excel reports with formatting, charts, and tracking sheets

**Report Features:**
- Multi-sheet workbook organization
- Conditional formatting
- Interactive charts and graphs
- Filterable data tables
- Application tracking
- Skills gap analysis

## Running Phase 6

```bash
jupyter notebook Excel_Integrate.ipynb
```

## Outputs

### excel_reports/ Directory

- `job_search_report_YYYYMMDD.xlsx` - Main report with job listings
- `application_tracker.xlsx` - Application tracking spreadsheet
- `excel_automation.log` - Generation logs

## Report Structure

### Sheet 1: Dashboard
- Summary statistics
- Top companies chart
- Skills distribution
- Location breakdown
- Salary range analysis
- Application deadline timeline

### Sheet 2: Top Recommendations
- Top 20 prioritized jobs
- Color-coded priority scores
- Key information highlighted
- Quick action buttons

### Sheet 3: All Opportunities
- Complete job listing
- Sortable and filterable columns
- Conditional formatting by score
- Search functionality

### Sheet 4: Application Tracker
- Job application status
- Application date
- Follow-up dates
- Interview stages
- Notes and comments
- Status indicators (Applied, Interview, Offer, Rejected)

### Sheet 5: Skills Gap Analysis
- Required skills frequency
- Your skills vs. market demand
- Skills to learn
- Certification recommendations

## Customization

### Modify Report Layout

Edit the notebook to customize:
- Sheet names and order
- Column visibility
- Color schemes
- Chart types
- Conditional formatting rules

### Example: Change Color Scheme

```python
# High priority (green)
HIGH_PRIORITY_COLOR = '00FF00'

# Medium priority (yellow)
MEDIUM_PRIORITY_COLOR = 'FFFF00'

# Low priority (red)
LOW_PRIORITY_COLOR = 'FF0000'
```

### Add Custom Sheets

```python
# Create new sheet
worksheet = workbook.add_worksheet('Custom Analysis')

# Add your data and formatting
worksheet.write('A1', 'Custom Data')
```

## Features

### Conditional Formatting

- **Priority Scores:** Color gradient (red → yellow → green)
- **Deadlines:** Urgent deadlines highlighted in red
- **Salary:** Above/below target highlighted
- **Application Status:** Color-coded status indicators

### Charts and Visualizations

- **Bar Chart:** Top companies by job count
- **Pie Chart:** Job type distribution
- **Line Chart:** Application deadline timeline
- **Scatter Plot:** Salary vs. priority score

### Data Validation

- **Application Status:** Dropdown list
- **Priority:** Dropdown (High/Medium/Low)
- **Follow-up Date:** Date picker

### Formulas

- Auto-calculate days until deadline
- Application success rate
- Average response time
- Skills match percentage

## Application Tracker Usage

### Status Workflow

1. **Not Applied** → Initial state
2. **Applied** → Application submitted
3. **Screening** → Resume screening stage
4. **Interview** → Interview scheduled/completed
5. **Offer** → Offer received
6. **Accepted** → Offer accepted
7. **Rejected** → Application rejected

### Tracking Tips

1. Update status immediately after each action
2. Set follow-up reminders
3. Add detailed notes for each interaction
4. Track interview questions and feedback
5. Monitor response times

## Troubleshooting

### Excel File Locked

```
Error: Permission denied
```
**Solution:** Close any open Excel files and try again

### Formatting Issues

If formatting doesn't appear:
- Ensure openpyxl and xlsxwriter are installed
- Check Excel version compatibility
- Try opening in different Excel version

### Large File Size

If report is too large:
- Reduce number of jobs included
- Remove unused sheets
- Compress images/charts
- Save as .xlsx instead of .xls

### Chart Not Displaying

```
Error: Chart data range invalid
```
**Solution:**
- Check data range references
- Ensure data exists in specified range
- Verify chart type compatibility

## Tips for Best Results

1. **Regular Updates:** Generate reports weekly during active job search
2. **Backup Reports:** Keep historical reports for comparison
3. **Share Selectively:** Remove sensitive data before sharing
4. **Print-Friendly:** Use page breaks and print settings
5. **Mobile Access:** Upload to OneDrive/Google Drive for mobile viewing

## Advanced Features

### Pivot Tables

Add pivot tables for advanced analysis:
```python
# Create pivot table
pivot = worksheet.add_pivot_table(
    data_range='A1:Z100',
    pivot_range='A1'
)
```

### Macros (VBA)

For Excel power users, add VBA macros:
- Auto-send follow-up emails
- Update status from email responses
- Generate weekly summary reports

### Integration

Connect with other tools:
- Export to Google Sheets
- Sync with Notion/Airtable
- Import to CRM systems
