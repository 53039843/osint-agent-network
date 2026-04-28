import logging
import sys
from core.config import settings

def setup_logger(name: str) -> logging.Logger:
    """Configures and returns a standard logger for the application."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        level = logging.DEBUG if settings.DEBUG_MODE else logging.INFO
        logger.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
