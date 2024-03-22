from util_common.datetime import format_now


def test_format_now():
    assert format_now().endswith('Z')
    assert not format_now(utc=False).endswith('Z')
