import os
import posixpath
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Tuple, Union

import natsort


def normalize_path(
    raw_path: Union[str, Path],
    name_process_fn: Optional[Callable] = None,
) -> Tuple[str, Path]:
    if isinstance(raw_path, str):
        raw_path = Path(raw_path).expanduser()
    name, parent, root = (
        raw_path.name,
        str(raw_path.parent),
        raw_path.root,
    )
    if name_process_fn is not None:
        name = name_process_fn(name)
    if root == '/':
        absolute_path = Path(parent).joinpath(name)
    elif parent == '.':
        absolute_path = get_absolute_cwd_path().joinpath(name)
    else:
        absolute_path = Path(
            posixpath.normpath(
                get_absolute_cwd_path().joinpath(parent).joinpath(name)
            )
        )
    return name, absolute_path


def get_absolute_cwd_path() -> Path:
    return Path(os.path.abspath(os.getcwd()))


def sort_paths(path_iter: Iterable[Path]) -> List[Path]:
    return natsort.natsorted(list(path_iter), key=lambda x: str(x))
