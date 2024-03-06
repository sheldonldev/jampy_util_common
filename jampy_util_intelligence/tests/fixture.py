import subprocess
from pathlib import Path

from pytest import fixture

from jampy_util.path import normalize_path


@fixture(scope="package")
def package_root_str():
    yield str(normalize_path(Path(__file__).parent.parent))


@fixture(scope="package")
def data_root_str():
    yield str(normalize_path(Path(__file__).parent.joinpath('data'))[1])


@fixture(scope="session", autouse=True)
def setup(package_root_str):
    reinstall(package_root_str)
    yield


def reinstall(root_str: str):
    subprocess.run(f"cd {root_str} && pip install .")
