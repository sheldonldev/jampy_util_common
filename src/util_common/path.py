import os
import posixpath
import shutil
from pathlib import Path
from typing import (
    Callable,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    get_args,
)

import natsort
from rich.prompt import Prompt

from ._log import log

ArchiveExt = Literal[
    "7z",
    "rar",
    "zip",
]
ARCHIVE_EXTS: List[ArchiveExt] = [*get_args(ArchiveExt)]

ImageExt = Literal[
    "jpg",
    "jpeg",
    "png",
]
IMAGE_EXTS: List[ImageExt] = [*get_args(ImageExt)]

PdfExt = Literal["pdf"]
PDF_EXTS: List[PdfExt] = [*get_args(PdfExt)]

WordExt = Literal[
    "doc",
    "docx",
]
WORD_EXTS: List[WordExt] = [*get_args(WordExt)]

ExcelExt = Literal[
    "xls",
    "xlsx",
]
EXCEL_EXTS: List[ExcelExt] = [*get_args(ExcelExt)]

OfficeExt = Union[WordExt, ExcelExt]
OFFICE_EXTS: List[OfficeExt] = WORD_EXTS + EXCEL_EXTS

DocumentExt = Union[ImageExt, PdfExt, OfficeExt]
DOCUMENT_EXTS: List[DocumentExt] = IMAGE_EXTS + PDF_EXTS + OFFICE_EXTS

FileExt = Union[ArchiveExt, ImageExt, PdfExt, OfficeExt]
FILE_EXTS: List[FileExt] = ARCHIVE_EXTS + IMAGE_EXTS + PDF_EXTS + OFFICE_EXTS

IGNORE_NAMES = [
    "__MACOSX",
    ".DS_Store",
]


def normalize_path(
    raw_path: str | Path,
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
                get_absolute_cwd_path().joinpath(parent).joinpath(name),
            )
        )
    return name, absolute_path


def get_absolute_cwd_path() -> Path:
    return Path(os.path.abspath(os.getcwd()))


def sort_paths(path_iter: Iterable[str | Path]) -> List[Path]:
    return [
        Path(x)
        for x in natsort.natsorted(
            list(path_iter),
            key=lambda x: str(x),
        )
    ]


def ensure_dir(
    path: Path | str,
    force_replace_file: bool = False,
    force_use_parent: bool = False,
) -> Path:
    path = Path(path)
    if path.exists() and path.is_file():
        log.warning(f"{path} is already exists, but IsFile!")
        if force_replace_file == force_use_parent:
            while True:
                remove = Prompt.ask(
                    """Choose an option:
                    1. remove the file.
                    2. use the parent folder.
                    3. exit.
                    """
                )
                if remove == "1":
                    os.remove(path)
                if remove == "2":
                    return path.parent
                if remove == "3":
                    exit()
        elif force_replace_file:
            log.warning(
                "In FORCE_REPLACE_FILE mode, the file has been removed!",
            )
            os.remove(path)
        else:
            log.warning(
                "In FORCE_USE_PARENT mode, the file has been removed!",
            )
            return path.parent

    path.mkdir(parents=True, exist_ok=True)
    return path


def clear_dir(path: Path | str) -> Path:
    path = Path(path)
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
    return ensure_dir(path, force_replace_file=True)


def get_parent(path: str | Path) -> str:
    return os.path.dirname(str(path))


def get_basename(path: str | Path) -> str:
    return os.path.basename(str(path))


def split_basename(path: str | Path) -> Tuple[str, str]:
    name, ext = os.path.splitext(get_basename(path))
    return name, ext.strip(".")


def get_basename_without_extension(path: str | Path) -> str:
    return split_basename(path)[0]


def get_extension(path: str | Path) -> str:
    return split_basename(path)[1]


def guess_extension_from_mime(mime: str) -> Optional[FileExt]:
    if "zip" in mime:
        return "zip"

    if "rar" in mime:
        return "rar"

    if "7z" in mime:
        return "7z"

    if "word" in mime and "document" not in mime:
        return "doc"

    if "word" in mime and "document" in mime:
        return "docx"

    if "excel" in mime:
        return "xls"

    if "sheet" in mime:
        return "xlsx"

    if "jpeg" in mime or "jpg" in mime:
        return "jpg"

    if "png" in mime:
        return "png"

    if "pdf" in mime:
        return "pdf"

    return None


def recursive_list_named_children(
    folder: str | Path,
    filename: str,
) -> Iterable[Path]:
    paths = Path(folder).glob(f"**/{filename}")
    return paths


def recursive_list_file(folder: str | Path) -> Iterable[Path]:
    for root, _, files in os.walk(folder):
        for file_name in [x for x in files if x not in IGNORE_NAMES]:
            yield Path(os.path.join(root, file_name))
