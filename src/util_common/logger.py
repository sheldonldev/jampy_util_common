import logging
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Sequence

import colorlog
from pydantic import BaseModel
from pythonjsonlogger import jsonlogger
from rich.logging import RichHandler

_LogLevel = Literal[
    "debug",
    "info",
    "warning",
    "error",
]

LOG_KEYS = [
    "asctime",
    "levelname",
    "name",
    "filename",
    "lineno",
    "process",
    "message",
]

LOG_FORMAT = (
    "%(blue)s%(asctime)sZ%(reset)s | "
    "%(log_color)s%(levelname)s%(reset)s | "
    "%(cyan)s%(name)s:"
    "%(filename)s:"
    "%(lineno)s%(reset)s | "
    "%(log_color)s%(process)d >>> "
    "%(message)s%(reset)s"
)

DEFAULT_LEVEL: _LogLevel = "info"


class LogSettings(BaseModel):
    name: Optional[str] = None
    level: _LogLevel = DEFAULT_LEVEL
    save_file_or_dir: Optional[Path] = None
    rich_handler: bool = False
    json_logger: bool = False


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        unwanted_keys = set(log_record.keys()) - set(LOG_KEYS)
        for k in unwanted_keys:
            del log_record[k]


def get_stream_handler() -> logging.StreamHandler:
    formatter = colorlog.ColoredFormatter(LOG_FORMAT)
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    return stream_handler


def setup_loggers(log_settings_list: Sequence[Optional[LogSettings]]) -> None:
    setup_basic_log_config()
    for log_settings in log_settings_list:
        configure_logger(log_settings)


def setup_logger(log_settings: Optional[LogSettings] = None) -> None:
    setup_basic_log_config()
    configure_logger(log_settings)


def configure_logger(log_settings: Optional[LogSettings]) -> None:
    if log_settings is None:
        log_settings = LogSettings()
    _configure_logger(log_settings)


def setup_basic_log_config() -> None:
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S")
    logging.Formatter.converter = time.gmtime


def _configure_logger(
    log_settings: LogSettings,
) -> None:
    logger = _init_logger(log_settings.name, log_settings.level)

    if log_settings.rich_handler is True:
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
    else:
        logger.addHandler(get_stream_handler())

    if log_settings.save_file_or_dir is not None:
        log_file = _create_log_file(
            log_settings.save_file_or_dir,
            log_settings.name,
        )
        file_handler = RotatingFileHandler(
            filename=str(log_file),
            maxBytes=1048576,
            backupCount=8,
        )
        if log_settings.json_logger is True:
            file_handler.setFormatter(CustomJsonFormatter(LOG_FORMAT))
        else:
            file_handler.setFormatter(colorlog.ColoredFormatter(LOG_FORMAT))
        logger.addHandler(file_handler)


def _init_logger(
    name: Optional[str] = None,
    level: _LogLevel = DEFAULT_LEVEL,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers.clear()
    logger.propagate = False
    return logger


def _create_log_file(log_path: Path, name: Optional[str]) -> Path:
    if log_path.is_dir():
        if name is None:
            log_path = log_path.joinpath("log")
        else:
            log_path = log_path.joinpath(f"{name}.log")
    log_path.parent.mkdir(exist_ok=True, parents=True)
    return log_path
