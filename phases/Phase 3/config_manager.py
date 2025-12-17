"""
Configuration Management for Phase 3 Entity Structuring
Handles loading, validation, and management of all Phase 3 settings.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger("ConfigurationManager")


class ConfigurationManager:
    """
    Manages configuration for Phase 3 Entity Structuring Pipeline.
    Handles loading, validation, and default configuration creation.
    """
    
    DEFAULT_CONFIG = {
        "incremental_processing": {
            "enabled": True,
            "state_directory": "state",
            "state_file": "processed_message_ids.txt",
            "checkpoint_interval": 50,
            "force_full_reprocess": False
        },
        "input_output": {
            "input_file": "../Phase 2/relevant_placement_emails.csv",
            "output_csv": "structured_job_postings.csv",
            "output_json": "structured_job_postings.json"
        },
        "processing": {
            "max_jobs_per_email": 5,
            "min_completeness_score": 0.3,
            "enable_analytics": True,
            "max_companies_per_email": 3,
            "max_positions_per_email": 3
        },
        "logging": {
            "level": "INFO",
            "file": "entity_structuring.log",
            "enable_performance_metrics": True
        },
        "normalization": {
            "skill_map": {
                "js": "javascript",
                "ts": "typescript",
                "py": "python",
                "reactjs": "react",
                "nodejs": "node.js",
                "ml": "machine learning",
                "ai": "artificial intelligence",
                "dl": "deep learning",
                "nlp": "natural language processing",
                "cv": "computer vision",
                "k8s": "kubernetes",
                "tf": "tensorflow",
                "scikit": "scikit-learn"
            },
            "degree_map": {
                "btech": "B.Tech",
                "b.tech": "B.Tech",
                "be": "B.E",
                "b.e": "B.E",
                "mtech": "M.Tech",
                "m.tech": "M.Tech",
                "me": "M.E",
                "m.e": "M.E",
                "bca": "BCA",
                "mca": "MCA",
                "bsc": "B.Sc",
                "b.sc": "B.Sc",
                "msc": "M.Sc",
                "m.sc": "M.Sc"
            },
            "city_map": {
                "bangalore": "Bangalore",
                "bengaluru": "Bangalore",
                "blr": "Bangalore",
                "mumbai": "Mumbai",
                "bombay": "Mumbai",
                "delhi": "Delhi",
                "new delhi": "Delhi",
                "ncr": "Delhi NCR",
                "gurgaon": "Gurgaon",
                "gurugram": "Gurgaon",
                "hyderabad": "Hyderabad",
                "pune": "Pune",
                "chennai": "Chennai",
                "kolkata": "Kolkata",
                "calcutta": "Kolkata"
            },
            "company_suffixes": [
                "PVT LTD",
                "PVT. LTD.",
                "PRIVATE LIMITED",
                "LIMITED",
                "LTD",
                "INC",
                "CORP",
                "CORPORATION",
                "LLC"
            ]
        },
        "position_levels": {
            "senior_keywords": ["senior", "lead", "principal", "staff"],
            "junior_keywords": ["junior", "associate", "entry"],
            "intern_keywords": ["intern", "trainee"],
            "manager_keywords": ["manager", "head", "director"]
        },
        "work_mode_keywords": {
            "remote": ["remote", "wfh", "work from home", "anywhere"],
            "hybrid": ["hybrid"]
        },
        "experience_types": {
            "fresher_keywords": ["fresher", "freshers", "entry level"],
            "thresholds": {
                "entry_level_max": 2,
                "mid_level_max": 5
            }
        },
        "salary_parsing": {
            "patterns": [
                {
                    "name": "lpa_range",
                    "pattern": r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?\s+per\s+annum)",
                    "confidence": 0.9
                },
                {
                    "name": "lpa_single",
                    "pattern": r"(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?\s+per\s+annum)",
                    "confidence": 0.85
                },
                {
                    "name": "monthly",
                    "pattern": r"(\d+)k?\s*(?:per\s+month|pm|/month)",
                    "confidence": 0.8
                },
                {
                    "name": "ctc",
                    "pattern": r"ctc\s*:?\s*(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?)",
                    "confidence": 0.85
                },
                {
                    "name": "package_range",
                    "pattern": r"package\s*:?\s*(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*lakhs?",
                    "confidence": 0.85
                }
            ],
            "default_currency": "INR",
            "default_period": "annual"
        },
        "experience_parsing": {
            "patterns": [
                r"(\d+)\s*(?:-|to)\s*(\d+)\s*years?",
                r"(\d+)\s*years?\s+(?:of\s+)?experience",
                r"0\s*(?:-|to)\s*(\d+)\s*years?"
            ]
        },
        "deadline_parsing": {
            "date_patterns": [
                {
                    "pattern": r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})",
                    "format": "%d-%m-%Y"
                },
                {
                    "pattern": r"(\d{1,2})[-/](\d{1,2})[-/](\d{2})",
                    "format": "%d-%m-%y"
                },
                {
                    "pattern": r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})",
                    "format": "%Y-%m-%d"
                }
            ],
            "relative_keywords": {
                "today": 0,
                "tomorrow": 1
            }
        }
    }
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file (default: config.json)
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger("ConfigurationManager")
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        Creates default config if file doesn't exist.
        
        Returns:
            Configuration dictionary
            
        Raises:
            ValueError: If configuration validation fails
        """
        # Check if config file exists
        if not os.path.exists(self.config_path):
            self.logger.warning(
                f"Configuration file not found at {self.config_path}"
            )
            self.logger.info("Creating default configuration file...")
            self.create_default_config()
            self.config = self.DEFAULT_CONFIG.copy()
        else:
            # Load existing config
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self.logger.info(
                    f"Configuration loaded from {self.config_path}"
                )
            except json.JSONDecodeError as e:
                self.logger.error(
                    f"Invalid JSON in configuration file: {e}"
                )
                self.logger.info("Creating new default configuration...")
                self.create_default_config()
                self.config = self.DEFAULT_CONFIG.copy()
            except Exception as e:
                self.logger.error(
                    f"Failed to load configuration file: {e}"
                )
                raise
        
        # Validate configuration
        if not self.validate_config(self.config):
            raise ValueError(
                "Configuration validation failed. "
                "Please check the error messages above."
            )
        
        # Log loaded settings
        self._log_configuration()
        
        return self.config
    
    def create_default_config(self) -> None:
        """
        Create default configuration file with example settings.
        """
        try:
            # Create directory if it doesn't exist
            config_dir = os.path.dirname(self.config_path)
            if config_dir:
                os.makedirs(config_dir, exist_ok=True)
            
            # Write default config with comments
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.DEFAULT_CONFIG, f, indent=2)
            
            self.logger.info(
                f"Default configuration file created at {self.config_path}"
            )
            self.logger.info(
                "Please review and modify the configuration as needed."
            )
        except Exception as e:
            self.logger.error(
                f"Failed to create default configuration file: {e}"
            )
            raise
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate configuration structure and values.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        is_valid = True
        
        # Check required top-level keys
        required_keys = [
            "incremental_processing",
            "input_output",
            "processing",
            "logging",
            "normalization",
            "position_levels",
            "work_mode_keywords",
            "experience_types",
            "salary_parsing",
            "experience_parsing",
            "deadline_parsing"
        ]
        
        for key in required_keys:
            if key not in config:
                self.logger.error(
                    f"Missing required configuration section: '{key}'"
                )
                is_valid = False
        
        if not is_valid:
            return False
        
        # Validate incremental_processing section
        is_valid &= self._validate_incremental_processing(
            config.get("incremental_processing", {})
        )
        
        # Validate input_output section
        is_valid &= self._validate_input_output(
            config.get("input_output", {})
        )
        
        # Validate processing section
        is_valid &= self._validate_processing(
            config.get("processing", {})
        )
        
        # Validate logging section
        is_valid &= self._validate_logging(
            config.get("logging", {})
        )
        
        # Validate normalization section
        is_valid &= self._validate_normalization(
            config.get("normalization", {})
        )
        
        # Validate position_levels section
        is_valid &= self._validate_position_levels(
            config.get("position_levels", {})
        )
        
        # Validate work_mode_keywords section
        is_valid &= self._validate_work_mode_keywords(
            config.get("work_mode_keywords", {})
        )
        
        # Validate experience_types section
        is_valid &= self._validate_experience_types(
            config.get("experience_types", {})
        )
        
        # Validate salary_parsing section
        is_valid &= self._validate_salary_parsing(
            config.get("salary_parsing", {})
        )
        
        # Validate experience_parsing section
        is_valid &= self._validate_experience_parsing(
            config.get("experience_parsing", {})
        )
        
        # Validate deadline_parsing section
        is_valid &= self._validate_deadline_parsing(
            config.get("deadline_parsing", {})
        )
        
        return is_valid
    
    def _validate_incremental_processing(
        self,
        section: Dict[str, Any]
    ) -> bool:
        """Validate incremental_processing configuration section."""
        is_valid = True
        
        # Check required fields
        required_fields = {
            "enabled": bool,
            "state_directory": str,
            "state_file": str,
            "checkpoint_interval": int,
            "force_full_reprocess": bool
        }
        
        for field, expected_type in required_fields.items():
            if field not in section:
                self.logger.error(
                    f"Missing required field in incremental_processing: "
                    f"'{field}'"
                )
                is_valid = False
            elif not isinstance(section[field], expected_type):
                self.logger.error(
                    f"Invalid type for incremental_processing.{field}: "
                    f"expected {expected_type.__name__}, "
                    f"got {type(section[field]).__name__}"
                )
                is_valid = False
        
        # Validate checkpoint_interval value
        if "checkpoint_interval" in section:
            interval = section["checkpoint_interval"]
            if not isinstance(interval, int) or interval <= 0:
                self.logger.error(
                    f"checkpoint_interval must be a positive integer, "
                    f"got {interval}"
                )
                is_valid = False
        
        return is_valid
    
    def _validate_input_output(self, section: Dict[str, Any]) -> bool:
        """Validate input_output configuration section."""
        is_valid = True
        
        # Check required fields
        required_fields = {
            "input_file": str,
            "output_csv": str,
            "output_json": str
        }
        
        for field, expected_type in required_fields.items():
            if field not in section:
                self.logger.error(
                    f"Missing required field in input_output: '{field}'"
                )
                is_valid = False
            elif not isinstance(section[field], expected_type):
                self.logger.error(
                    f"Invalid type for input_output.{field}: "
                    f"expected {expected_type.__name__}, "
                    f"got {type(section[field]).__name__}"
                )
                is_valid = False
        
        # Validate input file exists
        if "input_file" in section:
            input_path = section["input_file"]
            # Convert relative path to absolute based on Phase 3 directory
            if not os.path.isabs(input_path):
                phase3_dir = os.path.dirname(os.path.abspath(__file__))
                input_path = os.path.join(phase3_dir, input_path)
            
            if not os.path.exists(input_path):
                self.logger.warning(
                    f"Input file does not exist: {section['input_file']}"
                )
                self.logger.warning(
                    "Processing will fail if this file is not available."
                )
                # Don't mark as invalid - file might be created later
        
        return is_valid
    
    def _validate_processing(self, section: Dict[str, Any]) -> bool:
        """Validate processing configuration section."""
        is_valid = True
        
        # Check required fields
        required_fields = {
            "max_jobs_per_email": int,
            "min_completeness_score": (int, float),
            "enable_analytics": bool,
            "max_companies_per_email": int,
            "max_positions_per_email": int
        }
        
        for field, expected_type in required_fields.items():
            if field not in section:
                self.logger.error(
                    f"Missing required field in processing: '{field}'"
                )
                is_valid = False
            elif not isinstance(section[field], expected_type):
                type_name = (
                    expected_type.__name__ 
                    if not isinstance(expected_type, tuple)
                    else " or ".join(t.__name__ for t in expected_type)
                )
                self.logger.error(
                    f"Invalid type for processing.{field}: "
                    f"expected {type_name}, "
                    f"got {type(section[field]).__name__}"
                )
                is_valid = False
        
        # Validate max_jobs_per_email value
        if "max_jobs_per_email" in section:
            max_jobs = section["max_jobs_per_email"]
            if not isinstance(max_jobs, int) or max_jobs <= 0:
                self.logger.error(
                    f"max_jobs_per_email must be a positive integer, "
                    f"got {max_jobs}"
                )
                is_valid = False
        
        # Validate min_completeness_score value
        if "min_completeness_score" in section:
            min_score = section["min_completeness_score"]
            if not isinstance(min_score, (int, float)) or \
               not (0.0 <= min_score <= 1.0):
                self.logger.error(
                    f"min_completeness_score must be between 0.0 and 1.0, "
                    f"got {min_score}"
                )
                is_valid = False
        
        # Validate max_companies_per_email value
        if "max_companies_per_email" in section:
            max_companies = section["max_companies_per_email"]
            if not isinstance(max_companies, int) or max_companies <= 0:
                self.logger.error(
                    f"max_companies_per_email must be a positive integer, "
                    f"got {max_companies}"
                )
                is_valid = False
        
        # Validate max_positions_per_email value
        if "max_positions_per_email" in section:
            max_positions = section["max_positions_per_email"]
            if not isinstance(max_positions, int) or max_positions <= 0:
                self.logger.error(
                    f"max_positions_per_email must be a positive integer, "
                    f"got {max_positions}"
                )
                is_valid = False
        
        return is_valid
    
    def _validate_logging(self, section: Dict[str, Any]) -> bool:
        """Validate logging configuration section."""
        is_valid = True
        
        # Check required fields
        required_fields = {
            "level": str,
            "file": str,
            "enable_performance_metrics": bool
        }
        
        for field, expected_type in required_fields.items():
            if field not in section:
                self.logger.error(
                    f"Missing required field in logging: '{field}'"
                )
                is_valid = False
            elif not isinstance(section[field], expected_type):
                self.logger.error(
                    f"Invalid type for logging.{field}: "
                    f"expected {expected_type.__name__}, "
                    f"got {type(section[field]).__name__}"
                )
                is_valid = False
        
        # Validate log level
        if "level" in section:
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            level = section["level"].upper()
            if level not in valid_levels:
                self.logger.error(
                    f"Invalid log level: {section['level']}. "
                    f"Must be one of: {', '.join(valid_levels)}"
                )
                is_valid = False
        
        return is_valid
    
    def _validate_normalization(self, section: Dict[str, Any]) -> bool:
        """Validate normalization configuration section."""
        is_valid = True
        
        # Check required fields
        required_fields = {
            "skill_map": dict,
            "degree_map": dict,
            "city_map": dict,
            "company_suffixes": list
        }
        
        for field, expected_type in required_fields.items():
            if field not in section:
                self.logger.error(
                    f"Missing required field in normalization: '{field}'"
                )
                is_valid = False
            elif not isinstance(section[field], expected_type):
                self.logger.error(
                    f"Invalid type for normalization.{field}: "
                    f"expected {expected_type.__name__}, "
                    f"got {type(section[field]).__name__}"
                )
                is_valid = False
        
        return is_valid
    
    def _validate_position_levels(self, section: Dict[str, Any]) -> bool:
        """Validate position_levels configuration section."""
        is_valid = True
        
        # Check required fields
        required_fields = {
            "senior_keywords": list,
            "junior_keywords": list,
            "intern_keywords": list,
            "manager_keywords": list
        }
        
        for field, expected_type in required_fields.items():
            if field not in section:
                self.logger.error(
                    f"Missing required field in position_levels: '{field}'"
                )
                is_valid = False
            elif not isinstance(section[field], expected_type):
                self.logger.error(
                    f"Invalid type for position_levels.{field}: "
                    f"expected {expected_type.__name__}, "
                    f"got {type(section[field]).__name__}"
                )
                is_valid = False
        
        return is_valid
    
    def _validate_work_mode_keywords(self, section: Dict[str, Any]) -> bool:
        """Validate work_mode_keywords configuration section."""
        is_valid = True
        
        # Check required fields
        required_fields = {
            "remote": list,
            "hybrid": list
        }
        
        for field, expected_type in required_fields.items():
            if field not in section:
                self.logger.error(
                    f"Missing required field in work_mode_keywords: '{field}'"
                )
                is_valid = False
            elif not isinstance(section[field], expected_type):
                self.logger.error(
                    f"Invalid type for work_mode_keywords.{field}: "
                    f"expected {expected_type.__name__}, "
                    f"got {type(section[field]).__name__}"
                )
                is_valid = False
        
        return is_valid
    
    def _validate_experience_types(self, section: Dict[str, Any]) -> bool:
        """Validate experience_types configuration section."""
        is_valid = True
        
        # Check required fields
        if "fresher_keywords" not in section:
            self.logger.error(
                "Missing required field in experience_types: 'fresher_keywords'"
            )
            is_valid = False
        elif not isinstance(section["fresher_keywords"], list):
            self.logger.error(
                "Invalid type for experience_types.fresher_keywords: "
                f"expected list, got {type(section['fresher_keywords']).__name__}"
            )
            is_valid = False
        
        if "thresholds" not in section:
            self.logger.error(
                "Missing required field in experience_types: 'thresholds'"
            )
            is_valid = False
        elif not isinstance(section["thresholds"], dict):
            self.logger.error(
                "Invalid type for experience_types.thresholds: "
                f"expected dict, got {type(section['thresholds']).__name__}"
            )
            is_valid = False
        else:
            # Validate threshold values
            thresholds = section["thresholds"]
            for key in ["entry_level_max", "mid_level_max"]:
                if key not in thresholds:
                    self.logger.error(
                        f"Missing required field in experience_types.thresholds: '{key}'"
                    )
                    is_valid = False
                elif not isinstance(thresholds[key], int):
                    self.logger.error(
                        f"Invalid type for experience_types.thresholds.{key}: "
                        f"expected int, got {type(thresholds[key]).__name__}"
                    )
                    is_valid = False
        
        return is_valid
    
    def _validate_salary_parsing(self, section: Dict[str, Any]) -> bool:
        """Validate salary_parsing configuration section."""
        is_valid = True
        
        # Check required fields
        if "patterns" not in section:
            self.logger.error(
                "Missing required field in salary_parsing: 'patterns'"
            )
            is_valid = False
        elif not isinstance(section["patterns"], list):
            self.logger.error(
                "Invalid type for salary_parsing.patterns: "
                f"expected list, got {type(section['patterns']).__name__}"
            )
            is_valid = False
        else:
            # Validate each pattern
            for idx, pattern in enumerate(section["patterns"]):
                if not isinstance(pattern, dict):
                    self.logger.error(
                        f"Invalid pattern at index {idx}: expected dict"
                    )
                    is_valid = False
                    continue
                
                for key in ["name", "pattern", "confidence"]:
                    if key not in pattern:
                        self.logger.error(
                            f"Missing required field in pattern {idx}: '{key}'"
                        )
                        is_valid = False
        
        if "default_currency" not in section:
            self.logger.error(
                "Missing required field in salary_parsing: 'default_currency'"
            )
            is_valid = False
        
        if "default_period" not in section:
            self.logger.error(
                "Missing required field in salary_parsing: 'default_period'"
            )
            is_valid = False
        
        return is_valid
    
    def _validate_experience_parsing(self, section: Dict[str, Any]) -> bool:
        """Validate experience_parsing configuration section."""
        is_valid = True
        
        # Check required fields
        if "patterns" not in section:
            self.logger.error(
                "Missing required field in experience_parsing: 'patterns'"
            )
            is_valid = False
        elif not isinstance(section["patterns"], list):
            self.logger.error(
                "Invalid type for experience_parsing.patterns: "
                f"expected list, got {type(section['patterns']).__name__}"
            )
            is_valid = False
        
        return is_valid
    
    def _validate_deadline_parsing(self, section: Dict[str, Any]) -> bool:
        """Validate deadline_parsing configuration section."""
        is_valid = True
        
        # Check required fields
        if "date_patterns" not in section:
            self.logger.error(
                "Missing required field in deadline_parsing: 'date_patterns'"
            )
            is_valid = False
        elif not isinstance(section["date_patterns"], list):
            self.logger.error(
                "Invalid type for deadline_parsing.date_patterns: "
                f"expected list, got {type(section['date_patterns']).__name__}"
            )
            is_valid = False
        else:
            # Validate each date pattern
            for idx, pattern in enumerate(section["date_patterns"]):
                if not isinstance(pattern, dict):
                    self.logger.error(
                        f"Invalid date pattern at index {idx}: expected dict"
                    )
                    is_valid = False
                    continue
                
                for key in ["pattern", "format"]:
                    if key not in pattern:
                        self.logger.error(
                            f"Missing required field in date pattern {idx}: '{key}'"
                        )
                        is_valid = False
        
        if "relative_keywords" not in section:
            self.logger.error(
                "Missing required field in deadline_parsing: 'relative_keywords'"
            )
            is_valid = False
        elif not isinstance(section["relative_keywords"], dict):
            self.logger.error(
                "Invalid type for deadline_parsing.relative_keywords: "
                f"expected dict, got {type(section['relative_keywords']).__name__}"
            )
            is_valid = False
        
        return is_valid
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration setting by key path.
        
        Args:
            key: Dot-separated key path (e.g., "incremental_processing.enabled")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            self.logger.debug(
                f"Configuration key '{key}' not found, using default: {default}"
            )
            return default
    
    def _log_configuration(self) -> None:
        """Log loaded configuration settings for confirmation."""
        self.logger.info("=" * 70)
        self.logger.info("CONFIGURATION LOADED")
        self.logger.info("=" * 70)
        
        # Incremental processing settings
        inc_proc = self.config.get("incremental_processing", {})
        self.logger.info("Incremental Processing:")
        self.logger.info(f"  Enabled: {inc_proc.get('enabled')}")
        self.logger.info(
            f"  State Directory: {inc_proc.get('state_directory')}"
        )
        self.logger.info(f"  State File: {inc_proc.get('state_file')}")
        self.logger.info(
            f"  Checkpoint Interval: {inc_proc.get('checkpoint_interval')}"
        )
        self.logger.info(
            f"  Force Full Reprocess: {inc_proc.get('force_full_reprocess')}"
        )
        
        # Input/Output settings
        io_config = self.config.get("input_output", {})
        self.logger.info("Input/Output:")
        self.logger.info(f"  Input File: {io_config.get('input_file')}")
        self.logger.info(f"  Output CSV: {io_config.get('output_csv')}")
        self.logger.info(f"  Output JSON: {io_config.get('output_json')}")
        
        # Processing settings
        proc_config = self.config.get("processing", {})
        self.logger.info("Processing:")
        self.logger.info(
            f"  Max Jobs Per Email: {proc_config.get('max_jobs_per_email')}"
        )
        self.logger.info(
            f"  Max Companies Per Email: {proc_config.get('max_companies_per_email')}"
        )
        self.logger.info(
            f"  Max Positions Per Email: {proc_config.get('max_positions_per_email')}"
        )
        self.logger.info(
            f"  Min Completeness Score: "
            f"{proc_config.get('min_completeness_score')}"
        )
        self.logger.info(
            f"  Enable Analytics: {proc_config.get('enable_analytics')}"
        )
        
        # Logging settings
        log_config = self.config.get("logging", {})
        self.logger.info("Logging:")
        self.logger.info(f"  Level: {log_config.get('level')}")
        self.logger.info(f"  File: {log_config.get('file')}")
        self.logger.info(
            f"  Performance Metrics: "
            f"{log_config.get('enable_performance_metrics')}"
        )
        
        # Normalization settings
        norm_config = self.config.get("normalization", {})
        self.logger.info("Normalization:")
        self.logger.info(
            f"  Skill mappings: {len(norm_config.get('skill_map', {}))}"
        )
        self.logger.info(
            f"  Degree mappings: {len(norm_config.get('degree_map', {}))}"
        )
        self.logger.info(
            f"  City mappings: {len(norm_config.get('city_map', {}))}"
        )
        self.logger.info(
            f"  Company suffixes: {len(norm_config.get('company_suffixes', []))}"
        )
        
        # Position levels
        pos_config = self.config.get("position_levels", {})
        self.logger.info("Position Levels:")
        self.logger.info(
            f"  Senior keywords: {len(pos_config.get('senior_keywords', []))}"
        )
        self.logger.info(
            f"  Junior keywords: {len(pos_config.get('junior_keywords', []))}"
        )
        self.logger.info(
            f"  Intern keywords: {len(pos_config.get('intern_keywords', []))}"
        )
        self.logger.info(
            f"  Manager keywords: {len(pos_config.get('manager_keywords', []))}"
        )
        
        # Salary parsing
        salary_config = self.config.get("salary_parsing", {})
        self.logger.info("Salary Parsing:")
        self.logger.info(
            f"  Patterns: {len(salary_config.get('patterns', []))}"
        )
        self.logger.info(
            f"  Default currency: {salary_config.get('default_currency')}"
        )
        
        # Experience parsing
        exp_config = self.config.get("experience_parsing", {})
        self.logger.info("Experience Parsing:")
        self.logger.info(
            f"  Patterns: {len(exp_config.get('patterns', []))}"
        )
        
        # Deadline parsing
        deadline_config = self.config.get("deadline_parsing", {})
        self.logger.info("Deadline Parsing:")
        self.logger.info(
            f"  Date patterns: {len(deadline_config.get('date_patterns', []))}"
        )
        
        self.logger.info("=" * 70)


def create_example_config(output_path: str = "config.example.json") -> None:
    """
    Create an example configuration file with inline documentation.
    
    Args:
        output_path: Path where to save the example config
    """
    example_config = {
        "_comment": "Phase 3 Entity Structuring Configuration",
        "_description": "This file controls all Phase 3 processing behavior",
        
        "incremental_processing": {
            "_comment": "Incremental processing settings",
            "enabled": True,
            "_enabled_description": "Enable incremental processing (only process new emails)",
            
            "state_directory": "state",
            "_state_directory_description": "Directory to store state files",
            
            "state_file": "processed_message_ids.txt",
            "_state_file_description": "File name for tracking processed email IDs",
            
            "checkpoint_interval": 50,
            "_checkpoint_interval_description": "Save checkpoint every N emails for crash recovery",
            
            "force_full_reprocess": False,
            "_force_full_reprocess_description": "Set to true to reprocess all emails (ignores state)"
        },
        
        "input_output": {
            "_comment": "Input and output file paths",
            "input_file": "../Phase 2/relevant_placement_emails.csv",
            "_input_file_description": "Path to Phase 2 output CSV (relative to Phase 3 directory)",
            
            "output_csv": "structured_job_postings.csv",
            "_output_csv_description": "Output CSV file name",
            
            "output_json": "structured_job_postings.json",
            "_output_json_description": "Output JSON file name"
        },
        
        "processing": {
            "_comment": "Processing parameters",
            "max_jobs_per_email": 5,
            "_max_jobs_per_email_description": "Maximum job postings to extract per email",
            
            "min_completeness_score": 0.3,
            "_min_completeness_score_description": "Minimum completeness score (0.0-1.0) to include job",
            
            "enable_analytics": True,
            "_enable_analytics_description": "Generate analytics report after processing"
        },
        
        "logging": {
            "_comment": "Logging configuration",
            "level": "INFO",
            "_level_description": "Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
            
            "file": "entity_structuring.log",
            "_file_description": "Log file name",
            
            "enable_performance_metrics": True,
            "_enable_performance_metrics_description": "Log performance metrics and timing"
        }
    }
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(example_config, f, indent=2)
        print(f"Example configuration created at {output_path}")
    except Exception as e:
        print(f"Failed to create example configuration: {e}")


if __name__ == "__main__":
    # Test configuration manager
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    # Create example config
    create_example_config()
    
    # Test loading
    config_mgr = ConfigurationManager("config.json")
    config = config_mgr.load_config()
    
    print("\nConfiguration loaded successfully!")
    print(f"Incremental processing enabled: {config_mgr.get_setting('incremental_processing.enabled')}")
    print(f"Input file: {config_mgr.get_setting('input_output.input_file')}")
