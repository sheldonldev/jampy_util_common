from util_common._config import APP_NAME
from util_common._log import log
from util_common.logger import LogSettings, setup_logger

setup_logger(LogSettings(name=APP_NAME))

if __name__ == "__main__":
    log.info("log is available.")
