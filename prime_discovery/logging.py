"""Logging utilities for PrimeDiscoveryEngine.

Provides structured logging using loguru.
"""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger


class LoggerSetup:
    """Configure and manage application logging."""

    _initialized = False

    @classmethod
    def setup(
        cls,
        level: str = "INFO",
        log_dir: Optional[Path] = None,
        format_string: Optional[str] = None,
        rotation: str = "500 MB",
        retention: str = "7 days",
    ) -> None:
        """Setup logging configuration.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_dir: Directory for log files. If None, logs only to stderr
            format_string: Custom format string for log messages
            rotation: Log file rotation size
            retention: How long to keep log files
        """
        if cls._initialized:
            return

        # Remove default handler
        logger.remove()

        # Default format
        if format_string is None:
            format_string = (
                "<level>{time:YYYY-MM-DD HH:mm:ss}</level> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            )

        # Add stderr handler
        logger.add(
            sys.stderr,
            level=level,
            format=format_string,
            colorize=True,
        )

        # Add file handler if log_dir specified
        if log_dir:
            log_dir.mkdir(parents=True, exist_ok=True)
            logger.add(
                log_dir / "prime_discovery.log",
                level=level,
                format=format_string,
                rotation=rotation,
                retention=retention,
                colorize=False,
            )

        cls._initialized = True
        logger.debug(f"Logging initialized at level {level}")

    @classmethod
    def get_logger(cls):
        """Get the global logger instance.

        Returns:
            loguru logger instance
        """
        if not cls._initialized:
            cls.setup()
        return logger


def get_logger(name: str = __name__):
    """Get a logger instance with the given name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        loguru logger instance
    """
    return logger.bind(name=name)
