import logging
import os
from typing import Optional
from src.utils import dirs


def configure_logger(name: Optional[str] = 'main',
                     log_level: Optional[str] = 'DEBUG',
                     log_to_file: Optional[bool] = True,
                     log_file_path: Optional[str] = dirs.LOGS_DIR / 'logs.txt') -> logging.Logger:
    """
    Configures a logger with both console and file output.
    """
    # Create logger if it doesn't exist
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Set the log level dynamically
        numeric_level = getattr(logging, log_level.upper(), None)
        if numeric_level is None:
            raise ValueError(f'Invalid log level: {log_level}')
        logger.setLevel(numeric_level)

        # Create console handler with formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        # Add console handler to the logger
        logger.addHandler(console_handler)

        # Optionally, add a file handler
        if log_to_file:
            # Ensure the directory for log files exists
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            # Add file handler to the logger
            logger.addHandler(file_handler)

    return logger
