# Phase 4: Job Prioritization

## Overview

Phase 4 ranks and prioritizes job opportunities based on relevance, fit, and user preferences.

## Setup Instructions

### Required Inputs

- `../Phase 3/structured_job_postings.json` - Structured job data from Phase 3

### Dependencies

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install required packages
pip install pandas numpy scikit-learn
```

## Component

### job_prioritization.ipynb

**Purpose:** Score and rank jobs based on multiple criteria

**Scoring Criteria:**

1. **Skills Match (40%)**
   - Alignment with user's skill set
   - Required vs. preferred skills
   - Skill level matching

2. **Location Preference (20%)**
   - Geographic preference
   - Remote work availability
   - Relocation willingness

3. **Compensation (15%)**
   - Salary range alignment
   - Benefits package
   - Growth potential

4. **Company Reputation (10%)**
   - Company size and stability
   - Industry reputation
   - Growth trajectory

5. **Deadline Urgency (10%)**
   - Application deadline proximity
   - Time to prepare application
   - Competition level

6. **Job Type Match (5%)**
   - Full-time vs. internship preference
   - Contract vs. permanent
   - Experience level fit

## Configuration

You can customize scoring weights in the notebook:

```python
SCORING_WEIGHTS = {
    'skills_match': 0.40,
    'location': 0.20,
    'compensation': 0.15,
    'company': 0.10,
    'deadline': 0.10,
    'job_type': 0.05
}
```

### User Preferences

Set your preferences in the notebook:

```python
USER_PROFILE = {
    'skills': ['Python', 'Machine Learning', 'SQL', 'TensorFlow'],
    'preferred_locations': ['Remote', 'San Francisco', 'New York'],
    'min_salary': 60000,
    'max_salary': 120000,
    'job_types': ['Full-time', 'Internship'],
    'experience_level': 'Entry Level',
    'willing_to_relocate': True
}
```

## Running Phase 4

```bash
jupyter notebook job_prioritization.ipynb
```

## Outputs

- `prioritized_jobs.csv` - All jobs with priority scores (sorted by score)
- `top_recommendations.csv` - Top N recommended opportunities (default: top 20)
- `job_prioritization.log` - Scoring logs and statistics

## Output Format

### prioritized_jobs.csv

Contains all jobs with additional columns:
- `priority_score` - Overall score (0-100)
- `skills_score` - Skills match score
- `location_score` - Location preference score
- `compensation_score` - Salary alignment score
- `company_score` - Company reputation score
- `deadline_score` - Urgency score
- `job_type_score` - Job type match score
- `rank` - Overall ranking (1 = best match)

### top_recommendations.csv

Filtered to show only top opportunities with:
- All original job fields
- All scoring components
- Recommendation reason/summary

## Customization

### Adjusting Scoring Algorithm

1. **Change Weights:** Modify `SCORING_WEIGHTS` dictionary
2. **Add New Criteria:** Implement new scoring function
3. **Filter Results:** Add minimum score thresholds
4. **Boost Factors:** Add bonus points for specific criteria

### Example: Boost Remote Jobs

```python
if job['location']['remote']:
    job['location_score'] += 10  # Bonus points
```

## Quality Metrics

The notebook provides:
- Score distribution statistics
- Top companies by average score
- Skills gap analysis
- Location distribution
- Salary range analysis

## Troubleshooting

### All Scores Are Low

**Possible causes:**
- User profile doesn't match available jobs
- Scoring weights need adjustment
- Missing data in structured jobs

**Solution:**
- Review and update `USER_PROFILE`
- Adjust `SCORING_WEIGHTS`
- Check Phase 3 output quality

### Missing Scores

```
Error: NaN values in priority_score
```
**Solution:**
- Check for missing fields in input data
- Review `job_prioritization.log`
- Add default values for missing data

### Unexpected Rankings

If rankings seem off:
- Review individual score components
- Check scoring weight distribution
- Validate user preferences
- Examine outlier jobs manually

## Tips for Best Results

1. **Keep User Profile Updated:** Regularly update skills and preferences
2. **Adjust Weights Seasonally:** Prioritize deadline urgency during peak hiring
3. **Review Top 20:** Don't just focus on #1, review top recommendations
4. **Check Score Breakdown:** Understand why jobs rank high/low
5. **Iterate:** Adjust preferences based on results
