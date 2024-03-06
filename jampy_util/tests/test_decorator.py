import time

from jampy_util.decorator import tick_tock


def test_tick_tock():
    @tick_tock
    def sleep_seconds(s: int = 1):
        time.sleep(s)
    start = time.time()
    sleep_seconds()
    assert time.time() - start = 
