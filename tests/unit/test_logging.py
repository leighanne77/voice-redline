"""Test logging utility functions."""
import pytest
from app.utils.logging import logger, log_info, log_error, log_warning, log_debug
import logging

def test_logger_initialization():
    """Test logger is properly initialized."""
    assert logger.name == "voice_redline"
    assert logger.level <= 20  # INFO level or lower

def test_logging_functions():
    """Test logging utility functions."""
    # These should not raise exceptions
    log_info("Test info message")
    log_error("Test error message")
    log_warning("Test warning message")
    log_debug("Test debug message")

def test_log_handlers():
    """Test logger has proper handlers."""
    assert len(logger.handlers) >= 1
    assert any(handler.level <= logging.ERROR for handler in logger.handlers)