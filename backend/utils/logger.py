"""
Focus Friend - Structured Logger Utility.
Configures formatted console logging respecting configured log levels.
"""

import logging
import sys
import os


def setup_logger(name: str = "focus_friend") -> logging.Logger:
    """Configures a clean, structured console logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, log_level_name, logging.INFO)
        logger.setLevel(level)
    return logger


logger = setup_logger()
