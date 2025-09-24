import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


_CONFIGURED = False


def _configure_root_logger() -> None:
    """Configure root logger once with console and optional file handler.

    Honors environment variables:
    - LOG_LEVEL: logging level (default: INFO)
    - LOG_FILE: path to a rotating log file (optional)
    - LOG_FILE_MAX_BYTES: rotate at size in bytes (default: 5MB)
    - LOG_FILE_BACKUP_COUNT: number of rotated files to keep (default: 3)
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    root = logging.getLogger()
    root.setLevel(level)

    # Avoid duplicating handlers if something else configured logging already
    def _has_our_handler():
        for h in root.handlers:
            if getattr(h, "_smartitinerary", False):
                return True
        return False

    if not _has_our_handler():
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        # mark to detect later
        stream_handler._smartitinerary = True  # type: ignore[attr-defined]
        root.addHandler(stream_handler)

        log_file = os.getenv("LOG_FILE")
        if log_file:
            max_bytes = int(os.getenv("LOG_FILE_MAX_BYTES", str(5 * 1024 * 1024)))
            backup_count = int(os.getenv("LOG_FILE_BACKUP_COUNT", "3"))
            file_handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            file_handler._smartitinerary = True  # type: ignore[attr-defined]
            root.addHandler(file_handler)

    _CONFIGURED = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a configured logger.

    If name is None, returns a default project logger named 'SMARTITINERARY'.
    """
    _configure_root_logger()
    return logging.getLogger(name or "SMARTITINERARY")


__all__ = ["get_logger"]
