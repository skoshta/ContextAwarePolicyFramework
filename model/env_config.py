from dataclasses import dataclass
from typing import Dict, Any

from main import Environment
from model.security_policy import SecurityPolicy


@dataclass
class EnvironmentConfig:
    """Environment configuration structure"""
    name: str
    environment: Environment
    database: Dict[str, Any]
    api: Dict[str, Any]
    logging: Dict[str, Any]
    features: Dict[str, Any]
    security_policy: SecurityPolicy