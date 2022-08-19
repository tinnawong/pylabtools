import logging

def set_logfile(path_file: str, mode='a', encoding='utf-8'):
    """
    กำหนดค่าเริ่มสำหรับ log ที่ต้องการเขียน
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(path_file, mode, encoding)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s(%(levelname)s) - %(message)s'))
    root_logger.addHandler(handler)

def log_level(level: int, message: str, type=logging.INFO):
    "log message โดยจะ indent ตาม level"
    message = str(message)
    space = "\t"*(level-1)
    log_message = space+message
    if type == logging.INFO:
        logging.info(log_message)
    elif type == logging.ERROR:
        logging.error(log_message)
    elif type == logging.WARNING:
        logging.warning(log_message)
    else:
        logging.warning(log_message)