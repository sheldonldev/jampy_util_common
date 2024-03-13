from typing import Union


def parse_bool(value: Union[str, int, bool]) -> bool:
    if isinstance(value, bool) or isinstance(value, int):
        return bool(value)
    return value.lower().startswith("t") or value.lower().startswith("y")


def parse_int(value: Union[str, int, float]) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except Exception as e:
            raise e
