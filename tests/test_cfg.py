from util_common import _cfg
from util_common._log import log


def test_cfg():
    log.info("Testing config...")
    for name in dir(_cfg):
        attr = getattr(_cfg, name)
        if name.isupper() and not callable(attr):
            log.info(f"{name}: {attr}")
