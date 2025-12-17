import sys
import logging
from typing import Optional


class LoggerService:
    """
    Singleton Logger Service to handle application logging.
    """

    _instance: Optional["LoggerService"] = None
    _logger: logging.Logger

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        self._logger = logging.getLogger("AppLogger")
        self._logger.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Create file handler
        import os

        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        if not self._logger.handlers:
            self._logger.addHandler(console_handler)
            self._logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        return self._logger

    def log_info(self, message: str):
        self._logger.info(message)

    def log_error(self, message: str):
        self._logger.error(message)

    def log_warning(self, message: str):
        self._logger.warning(message)
