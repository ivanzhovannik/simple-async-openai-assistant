import logging
import sys

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def setup_logging(level: str = 'INFO') -> None:
    level = log_levels[level]
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stderr_handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[stderr_handler])