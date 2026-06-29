import logging
import sys


def _resolve_level(level_name: str | int) -> int:
    """Convert a string or integer log level into a logging constant."""
    if isinstance(level_name, int):
        return level_name

    normalized = level_name.strip().upper()

    mapping = logging.getLevelNamesMapping()
    if normalized in mapping:
        return mapping[normalized]

    raise ValueError(f"Invalid log level: {level_name}")


def bootstrap_logging(level_name: str | int = "INFO") -> logging.Logger:
    """Configure application logging.

    Safe to call multiple times without creating duplicate handlers.
    """

    level = _resolve_level(level_name)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not any(
        isinstance(handler, logging.StreamHandler)
        and handler.stream is sys.stdout
        for handler in root_logger.handlers
    ):
        handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(
            logging.Formatter(
                fmt=(
                    "%(asctime)s | %(levelname)s | "
                    "%(name)s | %(filename)s:%(lineno)d | "
                    "%(message)s"
                ),
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        root_logger.addHandler(handler)

    return logging.getLogger("product_tracker")


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced application logger."""
    return logging.getLogger(f"product_tracker.{name}")


logger = logging.getLogger("product_tracker")