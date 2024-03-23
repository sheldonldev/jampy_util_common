import time
from typing import Any, Callable


def ticktock(name=None):
    def decorator(fn: Callable):
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = fn(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(
                f"{fn.__name__ if name is None else name} elapsed time: {elapsed:.6f} secs"
            )
            return result

        return wrapper

    return decorator


def retry(max_attempts: int, delay: int):
    def decorator(fn: Callable):
        def wrapper(*args, **kwargs):
            attempts = 0
            error = None
            while attempts < max_attempts:
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        f'Attempt {attempts + 1} failed. Retrying {delay} seconds.'
                    )
                    attempts += 1
                    time.sleep(delay)
                    error = e
            raise Exception(f"Max attempts exceeded.\nError: {error}")

        return wrapper

    return decorator
