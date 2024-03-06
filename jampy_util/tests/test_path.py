from pathlib import Path

from jampy_util.path import get_absolute_cwd_path, parse_path_str


def test_get_absolute_cwd_path():
    cwd_path = get_absolute_cwd_path()
    assert isinstance(cwd_path, Path)
    assert str(cwd_path).startswith('/')
    assert './' not in str(cwd_path)


def test_parse_path_str():
    name, abs_path = parse_path_str('./')
    assert isinstance(name, str)
    assert isinstance(abs_path, Path)
    assert str(abs_path).endswith(name)
