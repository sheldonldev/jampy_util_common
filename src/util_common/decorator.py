import asyncio
import os
import time
from typing import Any, Callable

from ._log import log


def ticktock(name=None, print_fn=log.info):
    def decorator(fn: Callable):
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = await fn(*args, **kwargs)
            elapsed = time.time() - start_time
            print_fn(
                (fn.__name__ if name is None else name) + f" >>> Elapsed time: {elapsed:.6f} secs"
            )
            return result

        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = fn(*args, **kwargs)
            elapsed = time.time() - start_time
            print_fn(
                (fn.__name__ if name is None else name) + f" >>> Elapsed time: {elapsed:.6f} secs"
            )
            return result

        if asyncio.iscoroutinefunction(fn):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def retry(max_attempts: int, delay: int):
    def decorator(fn: Callable):
        async def async_wrapper(*args, **kwargs):
            attempts = 0
            error = None
            while attempts < max_attempts:
                try:
                    return await fn(*args, **kwargs)
                except Exception as e:
                    log.error(f">>> Attempt {attempts + 1} failed. " f"Retry in {delay} seconds.")
                    attempts += 1
                    await asyncio.sleep(delay)
                    error = e
            raise Exception(f">>> Max attempts exceeded.\nError: {error}")

        def sync_wrapper(*args, **kwargs):
            attempts = 0
            error = None
            while attempts < max_attempts:
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    log.error(f">>> Attempt {attempts + 1} failed. " f"Retry in {delay} seconds.")
                    attempts += 1
                    time.sleep(delay)
                    error = e
            raise Exception(f">>> Max attempts exceeded.\nError: {error}")

        if asyncio.iscoroutinefunction(fn):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def proxy(http_proxy: str = "", https_proxy: str = "", all_proxy: str = ""):
    def decorator(fn: Callable):
        async def async_wrapper(*args, **kwargs) -> Any:
            org_http_proxy = os.environ.get("http_proxy", "")
            org_https_proxy = os.environ.get("https_proxy", "")
            org_all_proxy = os.environ.get("all_proxy", "")
            os.environ["http_proxy"] = http_proxy
            os.environ["https_proxy"] = https_proxy
            os.environ["all_proxy"] = all_proxy
            try:
                result = await fn(*args, **kwargs)
            finally:
                os.environ["http_proxy"] = org_http_proxy
                os.environ["https_proxy"] = org_https_proxy
                os.environ["all_proxy"] = org_all_proxy
            return result

        def sync_wrapper(*args, **kwargs) -> Any:
            org_http_proxy = os.environ.get("http_proxy", "")
            org_https_proxy = os.environ.get("https_proxy", "")
            org_all_proxy = os.environ.get("all_proxy", "")
            os.environ["http_proxy"] = http_proxy
            os.environ["https_proxy"] = https_proxy
            os.environ["all_proxy"] = all_proxy
            try:
                result = fn(*args, **kwargs)
            finally:
                os.environ["http_proxy"] = org_http_proxy
                os.environ["https_proxy"] = org_https_proxy
                os.environ["all_proxy"] = org_all_proxy
            return result

        if asyncio.iscoroutinefunction(fn):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
