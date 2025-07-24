#!/usr/bin/env python3
"""
Environment Detection and Adaptive Policy Manager
Detects environment based on config files and Jenkins parameters
Applies context-based policies for different environments
"""

import json
import os
from typing import Dict, Any, Optional, List
from enum import Enum

from pathlib import Path


class Environment(Enum):
    DEV = "dev"
    QA = "qa"
    NON_PROD = "non-prod"
    PROD = "prod"

    def get_environment_specific_settings(self) -> Dict[str, Any]:
        """Get environment-specific application settings"""
        if not self.config:
            raise RuntimeError("Configuration not loaded. Call detect_and_load_environment() first.")

        return {
            'database_config': self.config.database,
            'api_config': self.config.api,
            'logging_config': self.config.logging,
            'feature_flags': self.config.features,
            'security_policy': self.apply_security_policies()
        }

    def validate_environment_compliance(self) -> List[str]:
        """Validate if current configuration complies with environment policies"""
        if not self.config:
            raise RuntimeError("Configuration not loaded.")

        violations = []
        policy = self.policies[self.current_env]

        # Check SSL configuration
        if policy.ssl_verification and not self.config.database.get('ssl', False):
            violations.append("SSL not enabled for database connection")

        # Check debug mode
        if not policy.debug_mode_allowed and self.config.api.get('debug', False):
            violations.append("Debug mode is not allowed in this environment")

        # Check logging level
        config_log_level = self.config.logging.get('level', 'INFO').upper()
        if config_log_level == 'DEBUG' and not policy.debug_mode_allowed:
            violations.append("Debug logging not allowed in this environment")

        return violations


def main():
    """Example usage of the environment detector"""
    # Create config directory and sample files
    detector = EnvironmentDetector()

    try:
        # Detect and load environment
        config = detector.detect_and_load_environment()

        print(f"Detected Environment: {config.environment.value}")
        print(f"Configuration: {config.name}")

        # Apply security policies
        policies = detector.apply_security_policies()
        print(f"Security Policies: {json.dumps(policies, indent=2)}")

        # Get environment-specific settings
        settings = detector.get_environment_specific_settings()
        print(f"Environment Settings: {json.dumps(settings, indent=2)}")

        # Validate compliance
        violations = detector.validate_environment_compliance()
        if violations:
            print(f"Compliance Violations: {violations}")
        else:
            print("Environment is compliant with security policies")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
