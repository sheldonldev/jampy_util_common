import os
import posixpath
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Tuple, Union

import natsort


class FileExtension(StrEnum):
    _7Z = "7z"
    RAR = "rar"
    ZIP = "zip"
    DOC = "doc"
    DOCX = "docx"
    XLS = "xls"
    XLSX = "xlsx"
    JPG = "jpg"
    PNG = "png"
    PDF = "pdf"


ARCHIVE_EXTS = [
    FileExtension._7Z.value,
    FileExtension.RAR.value,
    FileExtension.ZIP.value,
]
DOCUMENT_EXTS = [
    FileExtension.DOC.value,
    FileExtension.DOCX.value,
    FileExtension.XLS.value,
    FileExtension.XLSX.value,
    FileExtension.PNG.value,
    FileExtension.JPG.value,
    FileExtension.PDF.value,
]

IGNORE_NAMES = ["__MACOSX", ".DS_Store"]


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


def basename(path: str | Path) -> str:
    return os.path.basename(str(path))


def basename_without_extension(path: str | Path) -> str:
    return os.path.splitext(basename(path))[0]


def recursive_list_named_files(folder: str | Path, filename: str) -> List[str]:
    paths = Path(folder).glob(f'**/{filename}')
    return [str(path) for path in paths]
