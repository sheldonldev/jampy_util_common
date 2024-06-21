import json
from pathlib import Path

import pytest

from util_common._cfg import APP_NAME
from util_common._log import log
from util_common.logger import LogSettings, setup_logger
from util_common.path import clear_folder


@pytest.fixture(scope='module')
def log_dir(data_root: Path):
    yield clear_folder(data_root.joinpath('log'))


def test_log(log_dir: Path):
    setup_logger(
        LogSettings(
            name=APP_NAME,
            rich_handler=False,
            level='info',
            save_file_or_dir=log_dir,
        )
    )

    info_message = "Testing log..."
    log.info(info_message)

    assert log.name == APP_NAME
    log_path = log_dir.joinpath(f'{log.name}.log')
    assert log_path.exists()
    log_lines = log_path.read_text().splitlines()
    assert len(log_lines) == 1
    message = json.loads(log_lines[0]).get('message')
    assert message == info_message
