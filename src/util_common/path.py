import os
import posixpath
import shutil
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Tuple, Union

import natsort
from rich.prompt import Prompt

from ._log import log


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
    if root == "/":
        absolute_path = Path(parent).joinpath(name)
    elif parent == ".":
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


def ensure_dir(
    path: Path | str,
    force_replace_file: bool = False,
    force_use_parent: bool = False,
) -> Path:
    path = Path(path)
    if path.exists() and path.is_file():
        log.warning(f'{path} is already exists, but IsFile!')
        if force_replace_file == force_use_parent:
            while True:
                remove = Prompt.ask(
                    '''Choose an option:
                    1. remove the file.
                    2. use the parent folder.
                    3. exit.
                    '''
                )
                if remove == '1':
                    os.remove(path)
                if remove == '2':
                    return path.parent
                if remove == '3':
                    exit()
        elif force_replace_file:
            log.warning(
                'In FORCE_REPLACE_FILE mode, the file has been removed!',
            )
            os.remove(path)
        else:
            log.warning(
                'In FORCE_USE_PARENT mode, the file has been removed!',
            )
            return path.parent

    path.mkdir(parents=True, exist_ok=True)
    return path


def clear_dir(path: Path | str) -> Path:
    path = Path(path)
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
    return ensure_dir(path, force_replace_file=True)


def basename(path: str | Path) -> str:
    return os.path.basename(str(path))


def basename_without_extension(path: str | Path) -> str:
    return os.path.splitext(basename(path))[0]


def recursive_list_named_files(folder: str | Path, filename: str) -> List[str]:
    paths = Path(folder).glob(f"**/{filename}")
    return [str(path) for path in paths]
