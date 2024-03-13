import time
from math import isclose

from util_common.decorator import ticktock


def test_ticktock():
    @ticktock()
    def sleep_seconds(s: int = 1):
        time.sleep(s)

    start = time.time()
    sleep_seconds(1)
    end = time.time()
    assert isclose(end - start, 1, abs_tol=1e-2)
