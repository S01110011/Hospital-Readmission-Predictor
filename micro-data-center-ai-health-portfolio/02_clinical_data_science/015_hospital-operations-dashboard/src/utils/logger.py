"""Logging utilities."""

import logging
import sys


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Return a configured logger."""

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level.upper())
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    logger.addHandler(handler)
    return logger
