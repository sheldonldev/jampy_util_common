from typing import Dict

from jampy_util import package


def test_get_package_info():
    info = package.get_info('pip')
    assert isinstance(info, Dict)
    assert info.get('name') == 'pip'
