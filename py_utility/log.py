import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
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

def setup_logging(log_file_path: str ,mode='a', encoding='utf-8', log_level=logging.DEBUG) -> logging.Logger:
    """
    Sets up a logger with a JSON formatter and a file handler.

    Args:
        log_file_path (str): path to the log file.
        mode (str, optional): file mode. Defaults to 'a'.
        encoding (str, optional): file encoding. Defaults to 'utf-8'.
        log_level (int, optional): logging level. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: configured logger object.
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = JSONFormatter()

    file_handler = logging.FileHandler(log_file_path, mode=mode, encoding=encoding)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger