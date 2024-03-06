import logging
import time
from enum import StrEnum
from logging import Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import List, Optional, Tuple

import colorlog


class LogLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


def create_loggers(
    name_level_pairs: List[Tuple[Optional[str], LogLevel]],
    log_root: Path,
) -> None:
    _init_log_config()
    for name, level in name_level_pairs:
        _configure_logger(_init_logger(name), log_root, level)


def _init_log_config() -> None:
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S")
    logging.Formatter.converter = time.gmtime


def _configure_logger(
    logger: Logger,
    log_root: Path,
    level: LogLevel = LogLevel('error'),
) -> None:
    logger.setLevel(LOG_LEVELS[level.value])

    formatter = colorlog.ColoredFormatter(
        "%(white)s%(asctime)s UTC%(reset)s |"
        " %(log_color)s%(levelname)s%(reset)s |"
        " %(cyan)s%(name)s:%(filename)s:%(lineno)s%(reset)s |"
        " %(log_color)s%(process)d >>> %(message)s%(reset)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    for name, lvl in LOG_LEVELS.items():
        fhandler = RotatingFileHandler(
            _create_log_file(log_root, name),
            maxBytes=1048576,
            backupCount=8,
        )
        fhandler.setLevel(lvl)
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)


def _init_logger(name: Optional[str] = None) -> Logger:
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = False
    if name is not None:
        logging.info(f"Logger {name} initialized.")
    return logger


def _create_log_file(log_root: Path, log_type: str) -> str:
    log_root.mkdir(exist_ok=True, parents=True)
    return str(log_root.joinpath(f"{log_type}.log"))
