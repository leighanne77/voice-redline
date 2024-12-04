"""Logging configuration for the Voice Redline application."""
import logging
from functools import wraps
from typing import Any, Callable
from app.config import settings

# Create logger
logger = logging.getLogger("voice_redline")

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log")

# Create formatters and add it to handlers
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Set log level
logger.setLevel(getattr(logging, settings.log_level.upper()))

def log_error(message: str) -> None:
    """Log error message."""
    logger.error(message)

def log_info(message: str) -> None:
    """Log info message."""
    logger.info(message)

def log_warning(message: str) -> None:
    """Log warning message."""
    logger.warning(message)

def log_debug(message: str) -> None:
    """Log debug message."""
    logger.debug(message)

def log_function(func: Callable) -> Callable:
    """Decorator to log function entry and exit."""
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        log_info(f"Entering {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            log_info(f"Exiting {func.__name__}")
            return result
        except Exception as e:
            log_error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

# Export all logging utilities
__all__ = [
    'logger',
    'log_error',
    'log_info',
    'log_warning',
    'log_debug',
    'log_function'
] 