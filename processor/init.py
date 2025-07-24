from typing import Dict

from main import Environment
from model.security_policy import SecurityPolicy


def _load_security_policies(self) -> Dict[Environment, SecurityPolicy]:
    """Load security policies for different environments"""
    return {
        Environment.DEV: SecurityPolicy(
            encryption_required=False,
            ssl_verification=False,
            debug_mode_allowed=True,
            external_api_calls=True,
            logging_level="DEBUG",
            data_retention_days=7,
            backup_frequency="none"
        ),
        Environment.QA: SecurityPolicy(
            encryption_required=True,
            ssl_verification=True,
            debug_mode_allowed=True,
            external_api_calls=True,
            logging_level="INFO",
            data_retention_days=30,
            backup_frequency="weekly"
        ),
        Environment.NON_PROD: SecurityPolicy(
            encryption_required=True,
            ssl_verification=True,
            debug_mode_allowed=False,
            external_api_calls=False,
            logging_level="WARN",
            data_retention_days=90,
            backup_frequency="daily"
        ),
        Environment.PROD: SecurityPolicy(
            encryption_required=True,
            ssl_verification=True,
            debug_mode_allowed=False,
            external_api_calls=False,
            logging_level="ERROR",
            data_retention_days=365,
            backup_frequency="hourly"
        )
    }