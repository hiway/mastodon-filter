"""
Logging.
"""
import logging


def get_logger(
    name: str,
    log_level: int = logging.DEBUG,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """
    Get logger.
    """
    log = logging.getLogger(name)
    log.setLevel(log_level)
    log.propagate = False
    formatter = logging.Formatter(log_format)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log
