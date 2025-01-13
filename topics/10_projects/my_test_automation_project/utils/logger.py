import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name, log_file, level=logging.DEBUG):
    """
    Set up a logger that logs messages to both console and a file.
    
    Args:
        name (str): The name of the logger, typically the name of the module or test file.
        log_file (str): The path to the log file.
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG). Defaults to logging.INFO.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    log_directory = os.path.dirname(log_file)
    if log_directory and not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Create a logger instance
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if the logger is already set up
    if logger.hasHandlers():
        return logger

     # Create a file handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(level)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Define a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Explicitly flush and close the handlers after the test
    def close_handlers():
        for handler in logger.handlers:
            handler.flush()
            handler.close()

    # Attach the close_handlers function to be executed after the test finishes
    import atexit
    atexit.register(close_handlers)

    return logger
