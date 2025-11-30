import json
from typing import Any, Dict, Optional

class ConfigurationLoader:
    """
    Singleton Configuration Loader to manage application settings.
    """
    _instance: Optional['ConfigurationLoader'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigurationLoader, cls).__new__(cls)
        return cls._instance

    def load_configuration(self, file_path: str):
        """
        Loads configuration from a JSON file.
        """
        try:
            with open(file_path, 'r') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            print(f"Configuration file {file_path} not found. Using defaults.")
            self._config = {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}.")
            self._config = {}

    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value by key.
        """
        return self._config.get(key, default)
