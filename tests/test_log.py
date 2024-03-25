from util_common._cfg import APP_NAME
from util_common._log import log
from util_common.logger import LogSettings, setup_logger


def test_log():
    setup_logger(LogSettings(name=APP_NAME))
    log.info("log is available.")
