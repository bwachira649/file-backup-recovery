"""Logging configuration."""

import logging

from backup_manager.config import LOG_DIRECTORY, LOG_FILE


def configure_logging() -> None:
    """Configure application logging."""
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )