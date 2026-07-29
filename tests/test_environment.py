import pytest
from utils.logger import logger

def test_logger_initialization():
    """Verify that the logging module initializes correctly."""
    assert logger is not None
    logger.info("Environment test: Logger is working as expected.")

def test_environment_imports():
    """Verify that core dependencies are installed in the virtual environment."""
    import pandas
    import fastapi
    assert True