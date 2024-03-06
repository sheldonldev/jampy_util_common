import json
from typing import Dict


def json_to_bytes(json_: Dict, intent=4, ensure_ascii=False, encoding='utf-8'):
    return bytes(json.dumps(json_, indent=intent, ensure_ascii=ensure_ascii), encoding=encoding)


def str_to_bytes(text: str, encoding='utf-8'):
    return bytes(text, encoding=encoding)
