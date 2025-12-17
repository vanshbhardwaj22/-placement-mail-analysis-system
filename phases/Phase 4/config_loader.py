"""
Configuration Loader for Phase 4: Job Prioritization
Loads settings from config.json and creates UserProfile and PrioritizationWeights
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_path: Path to config.json file
        
    Returns:
        Dictionary containing configuration
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config


def create_user_profile_from_config(config: Dict[str, Any]):
    """
    Create UserProfile from config.json settings.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        UserProfile instance
    """
    from dataclasses import dataclass, field
    from typing import List, Set
    
    user_config = config.get('user_profile', {})
    
    # Extract user profile data
    user_id = "USER_CONFIG"
    name = "Config User"
    
    # Skills
    preferred_skills = user_config.get('preferred_skills', [])
    primary_skills = preferred_skills[:5]  # Top 5 as primary
    
    # Education
    degree = user_config.get('degree', 'B.Tech')
    education = [degree]
    
    # Experience
    exp_range = user_config.get('preferred_experience_range', {})
    experience_years = exp_range.get('min', 0)
    
    # Locations
    preferred_locations = user_config.get('preferred_locations', [])
    
    # Work mode
    preferred_work_modes = user_config.get('preferred_work_modes', [])
    preferred_work_mode = preferred_work_modes[0] if preferred_work_modes else 'Any'
    
    # Salary
    min_salary = user_config.get('min_salary_lpa', 0) * 100000  # Convert LPA to annual
    max_salary = user_config.get('max_salary_lpa', 50) * 100000
    
    # Avoid keywords
    avoid_keywords = user_config.get('avoid_keywords', [])
    
    return {
        'user_id': user_id,
        'name': name,
        'skills': preferred_skills,
        'primary_skills': primary_skills,
        'education': education,
        'experience_years': experience_years,
        'preferred_locations': preferred_locations,
        'preferred_work_mode': preferred_work_mode,
        'min_expected_salary': min_salary,
        'max_expected_salary': max_salary,
        'must_have_skills': primary_skills[:3],  # Top 3 as must-have
        'avoid_keywords': avoid_keywords,
        'preferred_companies': []
    }


def create_weights_from_config(config: Dict[str, Any]):
    """
    Create PrioritizationWeights from config.json settings.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary of weights
    """
    weights_config = config.get('scoring_weights', {})
    
    return {
        'skills_match_weight': weights_config.get('skills_match', 0.30),
        'experience_match_weight': weights_config.get('experience_fit', 0.05),
        'education_match_weight': 0.05,  # Not in config, using default
        'location_match_weight': weights_config.get('location_preference', 0.15),
        'completeness_weight': weights_config.get('completeness', 0.05),
        'salary_competitiveness_weight': weights_config.get('salary_attractiveness', 0.15),
        'company_reputation_weight': weights_config.get('company_reputation', 0.10),
        'deadline_urgency_weight': weights_config.get('deadline_urgency', 0.10),
        'posting_freshness_weight': 0.05,  # Not in config, using default
        'preference_bonus_weight': weights_config.get('work_mode_preference', 0.10)
    }


def get_input_output_paths(config: Dict[str, Any]) -> Dict[str, str]:
    """
    Get input/output file paths from config.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary with file paths
    """
    io_config = config.get('input_output', {})
    
    return {
        'input_file': io_config.get('input_file', '../Phase 3/structured_job_postings.json'),
        'output_csv': io_config.get('output_csv', 'prioritized_jobs.csv'),
        'top_recommendations_csv': io_config.get('top_recommendations_csv', 'top_recommendations.csv'),
        'top_n': io_config.get('top_n_recommendations', 20)
    }


def get_incremental_processing_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get incremental processing configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Incremental processing settings
    """
    inc_config = config.get('incremental_processing', {})
    
    return {
        'enabled': inc_config.get('enabled', True),
        'state_directory': inc_config.get('state_directory', 'state'),
        'state_file': inc_config.get('state_file', 'prioritized_job_ids.txt'),
        'checkpoint_interval': inc_config.get('checkpoint_interval', 50),
        'force_full_reprocess': inc_config.get('force_full_reprocess', False),
        'recalculate_all_priorities': inc_config.get('recalculate_all_priorities', False)
    }


def get_company_reputation_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get company reputation scoring configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Company reputation settings
    """
    rep_config = config.get('company_reputation', {})
    
    return {
        'tier_scores': rep_config.get('tier_scores', {}),
        'faang_companies': set(c.lower() for c in rep_config.get('faang_companies', [])),
        'unicorn_companies': set(c.lower() for c in rep_config.get('unicorn_companies', [])),
        'mnc_companies': set(c.lower() for c in rep_config.get('mnc_companies', []))
    }


def get_skills_scoring_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get skills scoring configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Skills scoring settings
    """
    skills_config = config.get('skills_scoring', {})
    
    return {
        'exact_match_bonus': skills_config.get('exact_match_bonus', 1.0),
        'partial_match_bonus': skills_config.get('partial_match_bonus', 0.5),
        'skill_categories': skills_config.get('skill_categories', {}),
        'min_skills_for_bonus': skills_config.get('min_skills_for_bonus', 3),
        'multiple_skills_bonus': skills_config.get('multiple_skills_bonus', 0.2)
    }


def get_location_scoring_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get location scoring configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Location scoring settings
    """
    loc_config = config.get('location_scoring', {})
    
    return {
        'exact_match_score': loc_config.get('exact_match_score', 1.0),
        'remote_score': loc_config.get('remote_score', 1.0),
        'tier1_cities_score': loc_config.get('tier1_cities_score', 0.8),
        'tier2_cities_score': loc_config.get('tier2_cities_score', 0.6),
        'other_cities_score': loc_config.get('other_cities_score', 0.4),
        'tier1_cities': set(c.lower() for c in loc_config.get('tier1_cities', [])),
        'tier2_cities': set(c.lower() for c in loc_config.get('tier2_cities', []))
    }


def get_salary_scoring_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get salary scoring configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Salary scoring settings
    """
    sal_config = config.get('salary_scoring', {})
    
    return {
        'ideal_salary_lpa': sal_config.get('ideal_salary_lpa', 8.0),
        'min_acceptable_lpa': sal_config.get('min_acceptable_lpa', 3.0),
        'max_expected_lpa': sal_config.get('max_expected_lpa', 15.0),
        'below_min_penalty': sal_config.get('below_min_penalty', 0.5),
        'above_max_bonus': sal_config.get('above_max_bonus', 0.2),
        'missing_salary_score': sal_config.get('missing_salary_score', 0.5)
    }


def get_deadline_urgency_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get deadline urgency configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Deadline urgency settings
    """
    deadline_config = config.get('deadline_urgency', {})
    
    return {
        'days_thresholds': deadline_config.get('days_thresholds', {}),
        'urgency_scores': deadline_config.get('urgency_scores', {}),
        'expired_penalty': deadline_config.get('expired_penalty', 0.0)
    }


def get_logging_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get logging configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Logging settings
    """
    log_config = config.get('logging', {})
    
    return {
        'level': log_config.get('level', 'INFO'),
        'file': log_config.get('file', 'job_prioritization.log'),
        'enable_performance_metrics': log_config.get('enable_performance_metrics', True)
    }


# Example usage
if __name__ == "__main__":
    # Load config
    config = load_config("config.json")
    
    # Create user profile
    user_profile_data = create_user_profile_from_config(config)
    print("User Profile:", user_profile_data)
    
    # Create weights
    weights_data = create_weights_from_config(config)
    print("\nWeights:", weights_data)
    
    # Get paths
    paths = get_input_output_paths(config)
    print("\nPaths:", paths)
