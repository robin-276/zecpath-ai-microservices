import logging
import os

def setup_logger(name: str = "zecpath_ai"):
    """
    Sets up a standardized logger for Zecpath AI activities.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        # Console output
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

# Global logger instance
logger = setup_logger()