import os
import posixpath
from pathlib import Path
from typing import Callable, Optional, Tuple


def parse_path_str(
    raw_path: str,
    name_process_fn: Optional[Callable] = None,
) -> Tuple[str, Path]:
    parsed_path = Path(raw_path).expanduser()
    name, parent, root = (
        parsed_path.name,
        str(parsed_path.parent),
        parsed_path.root,
    )
    if name_process_fn is not None:
        name = name_process_fn(name)
    if root == '/':
        absolute_path = Path(parent).joinpath(name)
    elif parent == '.':
        absolute_path = get_absolute_cwd_path().joinpath(name)
    else:
        absolute_path = Path(
            posixpath.normpath(get_absolute_cwd_path().joinpath(parent).joinpath(name))
        )
    return name, absolute_path


def get_absolute_cwd_path() -> Path:
    return Path(os.path.abspath(os.getcwd()))
