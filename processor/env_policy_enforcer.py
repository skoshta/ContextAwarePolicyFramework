"""
IAM Roles & Access - Non-prod: Relaxed, shared, Prod: Least privilege, restricted
CI/CD Gates - Non-prod: Fast, minimal checks, Prod: Manual approval, mandatory gates
Security Scanning - Non-prod: Optional or advisory, Prod: Blocking on fail
Logging & Monitoring - Non-prod: Minimal, Prod: Full audit, retention, alerting
Infrastructure Policy - Non-prod: Advisory, flexible, Prod: Mandatory enforcement (Sentinel/OPA)
Secrets - Non-prod: Mock or test secrets, Prod: Encrypted secrets with rotation
Change Controls - Non-prod: None or informal, Prod: Formal review, change window
"""


def apply_security_policies(self) -> Dict[str, Any]:
    """Apply security policies based on current environment"""
    if not self.current_env:
        raise RuntimeError("Environment not detected. Call detect_and_load_environment() first.")

    policy = self.policies[self.current_env]

    # Apply policies
    applied_policies = {
        'environment': self.current_env.value,
        'encryption_enabled': policy.encryption_required,
        'ssl_verification': policy.ssl_verification,
        'debug_mode': policy.debug_mode_allowed,
        'external_api_access': policy.external_api_calls,
        'log_level': policy.logging_level,
        'data_retention_days': policy.data_retention_days,
        'backup_schedule': policy.backup_frequency
    }

    self.logger.info(f"Applied security policies: {applied_policies}")
    return applied_policies
