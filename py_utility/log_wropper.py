import logging
from typing import Optional, Union
from pathlib import Path
import json

class JSONFormatter(logging.Formatter):
    """
    A custom formatter for logging messages as JSON.
    
    Methods:
        format: Returns the log message formatted as a JSON string.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Return the log message formatted as JSON."""
        log_data = {
            'timestamp': record.created,
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'line': record.lineno,
            'funcName': record.funcName,
            'pathname': record.pathname
        }
        return json.dumps(log_data, ensure_ascii=False)

class LoggerSetup:
    """
    A class to configure a logger with options for JSON formatted logging to file and console.
    
    Methods:
        add_file_handler: Adds a file handler to the logger.
        add_console_handler: Adds a console handler to the logger.
        set_custom_format: Sets a custom formatter for logging messages.
        get_logger: Returns the configured logger.
    """
    
    def __init__(self, log_level: int = logging.DEBUG):
        """Initialize the LoggerSetup with the desired log level.
        
        Examples:
        >>> logger_setup = LoggerSetup(log_level=logging.DEBUG)
        >>> custom_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        >>> logger_setup.set_custom_format(custom_format)
        >>> logger_setup.add_file_handler("logfile.log")
        >>> logger_setup.add_console_handler()
        >>> logger = logger_setup.get_logger()
        >>> logger.debug("This is a debug message.")
        """
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)
        self.formatter = JSONFormatter()

    def add_file_handler(self, log_file_path: Optional[Path] = None, mode: str = 'a', encoding: str = 'utf-8') -> None:
        """
        Add a file handler to the logger.

        Args:
            log_file_path (Path): The path to the log file. Defaults to None.
            mode (str): File mode. Defaults to 'a'.
            encoding (str): File encoding. Defaults to 'utf-8'.
        """
        if log_file_path:
            file_handler = logging.FileHandler(log_file_path, mode=mode, encoding=encoding)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

    def add_console_handler(self) -> None:
        """Add a console handler to the logger."""
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def set_custom_format(self, fmt: Union[logging.Formatter, None]) -> None:
        """
        Set a custom formatter for logging messages.

        Args:
            fmt (logging.Formatter | None): The desired logging formatter.
        """
        for handler in self.logger.handlers:
            handler.setFormatter(fmt)
        self.formatter = fmt

    def get_logger(self) -> logging.Logger:
        """Return the configured logger."""
        return self.logger
