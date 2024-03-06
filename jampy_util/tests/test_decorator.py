import time
from math import isclose

from jampy_util.decorator import ticktock


def test_ticktock():
    @ticktock
    def sleep_seconds(s: int = 1):
        time.sleep(s)

    start = time.time()
    sleep_seconds()
    assert isclose(time.time() - start, 1, abs_tol=1e-1)
