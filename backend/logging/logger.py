import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(name, level=logging.INFO):
    """
    Function to setup a logger with a dynamically named log file based on timestamp.
    
    Parameters:
    - name: The name of the logger, usually `__name__` from the calling module.
    - level: The logging level (default is logging.INFO).
    
    Returns:
    - logger: Configured logger instance.
    """
    # Create a timestamped log file name
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '-py_app.log'
    
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create a rotating file handler (logs will rotate when they reach 5MB)
    handler = RotatingFileHandler(log_filename, maxBytes=5*1024*1024, backupCount=5)
    handler.setLevel(level)
    
    # Create a console handler to log to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create a formatter that includes the module name dynamically
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    
    # Set the formatter for both handlers
    handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger(__name__)