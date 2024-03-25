from pathlib import Path

import pytest

DATA_ROOT = Path(__file__).parent.joinpath('data')


@pytest.fixture(scope='session')
def data_root():
    yield DATA_ROOT


def pytest_sessionstart(session: pytest.Session):
    pass
