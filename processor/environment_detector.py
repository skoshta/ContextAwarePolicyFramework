import json
import os
import yaml
from pathlib import Path
from typing import Optional

from main import Environment
from model.env_config import EnvironmentConfig


def _get_jenkins_file_path (project_root: Path) -> Optional[Path]:
    """
    Searches the root of the given project directory for a Jenkins YAML file.

    :param project_root: Path to the project root directory
    :return: Path to the Jenkins YAML file if found, else None
    """
    root = Path(project_root).resolve().parent.parent  # Get root folder
    jenkins_yaml_names = ['jenkins', 'jenkins.yaml', 'jenkinsfile', 'jenkinsfile.yaml', 'deploy.yml']

    for file_name in jenkins_yaml_names:
        candidate = root / file_name
        if candidate.is_file():
            return candidate

    return None


class EnvironmentDetector:
    """Main class for environment detection and policy management"""

    def __init__(self, config_dir: str = "config"):
        self.jenkins_file = Path(config_dir)
        self.logger = self._setup_logging()
        self.current_env = None
        self.config = None
        self.policies = self._load_security_policies()

    def get_target_environments_choices(self) -> []:
        """
        Parses a Jenkins pipeline YAML to extract deployment environment choices from
        the TARGET_ENVIRONMENTS param

        :return: List of deploy envs
        """

        with open(self.jenkins_file, 'r') as file:
            data = yaml.safe_load(file)

        # Navigate to the params section
        params = data.get("pipeline", {}).get("parameters", [])
        for param in params:
            if 'choice' in param and param['choice'].get['name'] == 'TARGET_ENVIRONMENTS':
                return param['choice'].get('choices', [])

        return [] # if choices not found
