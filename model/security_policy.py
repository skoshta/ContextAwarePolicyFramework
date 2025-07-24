from dataclasses import dataclass

@dataclass
class SecurityPolicy:
    """Security policy configuration for different environments"""
    encryption_required: bool
    ssl_verification: bool
    debug_mode_allowed: bool
    external_api_calls: bool
    logging_level: str
    data_retention_days: int
    backup_frequency: str