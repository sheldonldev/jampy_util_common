from jampy_util import format_now


def test_format_now():
    assert 'UTC' in format_now()
    assert 'UTC' not in format_now(utc=False)
