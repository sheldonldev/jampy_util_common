import logging
import time
from contextlib import suppress
from enum import Enum
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from pydantic import BaseModel
from pythonjsonlogger import jsonlogger
from rich.logging import RichHandler


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


LOG_FORMAT = (
    "%(asctime)s"
    "%(levelname)s"
    "%(name)s"
    "%(filename)s"
    "%(lineno)s"
    "%(process)d"
    "%(message)s"
)

DEFAULT_LEVEL = LogLevel.INFO


class LogSettings(BaseModel):
    name: Optional[str] = None
    level: LogLevel = DEFAULT_LEVEL
    save_file_or_dir: Optional[Path] = None


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        with suppress(KeyError):
            del log_record['color_message']


def setup_loggers(log_settings_list: Sequence[Optional[LogSettings]]):
    setup_basic_log_config()
    for log_settings in log_settings_list:
        configure_logger(log_settings)


def setup_logger(log_settings: Optional[LogSettings] = None):
    setup_basic_log_config()
    configure_logger(log_settings)


def configure_logger(log_settings: Optional[LogSettings]):
    if log_settings is None:
        _configure_logger()
    else:
        _configure_logger(
            log_settings.name, log_settings.level, log_settings.save_file_or_dir
        )


def setup_basic_log_config() -> None:
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S")
    logging.Formatter.converter = time.gmtime


def _configure_logger(
    name: Optional[str] = None,
    level: LogLevel = DEFAULT_LEVEL,
    save_file_or_dir: Optional[Path] = None,
) -> None:
    logger = _init_logger(name, level)

    logger.addHandler(
        RichHandler(
            rich_tracebacks=True,
            show_time=True,
            omit_repeated_times=True,
            show_level=True,
            show_path=True,
            enable_link_path=True,
        )
    )
    if save_file_or_dir is not None:
        log_file = _create_log_file(save_file_or_dir)
        file_handler = RotatingFileHandler(
            filename=str(log_file),
            maxBytes=1048576,
            backupCount=8,
        )
        file_handler.setFormatter(CustomJsonFormatter(LOG_FORMAT))
        logger.addHandler(file_handler)


def _init_logger(
    name: Optional[str] = None,
    level: LogLevel = DEFAULT_LEVEL,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.value.upper()))
    logger.handlers.clear()
    logger.propagate = False
    return logger


def _create_log_file(log_path: Path) -> Path:
    if log_path.is_dir():
        log_path = log_path.joinpath('log')
    log_path.parent.mkdir(exist_ok=True, parents=True)
    return log_path
