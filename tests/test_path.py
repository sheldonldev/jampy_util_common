from pathlib import Path

from util_common.path import get_absolute_cwd_path, normalize_path


def test_get_absolute_cwd_path():
    cwd_path = get_absolute_cwd_path()
    assert isinstance(cwd_path, Path)
    assert str(cwd_path).startswith('/')
    assert './' not in str(cwd_path)


def test_normalize_path():
    name, abs_path = normalize_path('./')
    assert isinstance(name, str)
    assert isinstance(abs_path, Path)
    assert str(abs_path).endswith(name)
