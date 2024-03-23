from util_common import _config

if __name__ == '__main__':
    for name in dir(_config):
        attr = getattr(_config, name)
        if name.isupper() and not callable(attr):
            print(f"{name}: {attr}")
