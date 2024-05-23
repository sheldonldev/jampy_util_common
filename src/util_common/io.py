import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import magic
import patoolib  # type: ignore

from ._log import log
from .path import (
    ARCHIVE_EXTS,
    DOCUMENT_EXTS,
    IGNORE_NAMES,
    FileExt,
    get_basename_without_extension,
    guess_extension_from_mime,
)


def json_to_bytes(
    json_: Dict | List[Dict], intent=4, ensure_ascii=False, encoding="utf-8"
) -> bytes:
    return bytes(
        json.dumps(json_, indent=intent, ensure_ascii=ensure_ascii),
        encoding=encoding,
    )


def str_to_bytes(text: str, encoding="utf-8") -> bytes:
    return bytes(text, encoding=encoding)


def parse_bool(value: str | int | bool) -> bool:
    if isinstance(value, bool) or isinstance(value, int):
        return bool(value)
    return value.lower().startswith("t") or value.lower().startswith("y")


def parse_int(value: str | int | float) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except Exception as e:
            raise e


def guess_file_extension(file: bytes) -> Optional[FileExt]:
    # TODO: 如果结果与实际不符，需要进一步更正。
    # 用libreoffice 查看media-type:
    # https://wiki.documentfoundation.org/Macros/Python_Guide/Introduction

    mime = magic.from_buffer(file, mime=True).lower()
    ext = guess_extension_from_mime(mime)
    return ext


def recursive_yield_file_bytes(
    folder_path: str | Path,
    include_archive_exts: Sequence[FileExt] = ARCHIVE_EXTS,
    include_document_exts: Sequence[FileExt] = DOCUMENT_EXTS,
) -> Iterable[Tuple[bytes, FileExt]]:
    """Recursively yield file bytes from a folder.

    include_archive_exts:
       if archive is included, the archive will be treated as folder.
    include_document_exts:
        only matched document type will be yield.
    """
    for root, _, files in os.walk(folder_path):
        for file_name in [x for x in files if x not in IGNORE_NAMES]:
            file_path = os.path.join(root, file_name)
            file_bytes = Path(file_path).read_bytes()
            ext = guess_file_extension(file_bytes)
            file_name = f"{get_basename_without_extension(file_name)}.{ext}"
            if ext is not None and ext in include_document_exts:
                yield file_bytes, file_name

            if ext in include_archive_exts:
                for _file_bytes, _file_name in yield_files_from_archive(
                    file_bytes,
                    include_archive_exts=include_archive_exts,
                    include_document_exts=include_document_exts,
                    recursive=True,
                ):
                    yield _file_bytes, _file_name


def yield_files_from_archive(
    archive: bytes,
    password: Optional[str] = None,
    include_archive_exts: Sequence[FileExt] = ARCHIVE_EXTS,
    include_document_exts: Sequence[FileExt] = DOCUMENT_EXTS,
    recursive: bool = False,
) -> Iterable[Tuple[bytes, FileExt]]:
    """Yield file bytes from archive

    include_exts:
        only matched type of archive will be processed.
    recursive:
        if True, nested archive will be processed.
    """
    arch_suffix = guess_file_extension(archive)
    if isinstance(arch_suffix, str) and arch_suffix in ARCHIVE_EXTS:

        tmp_prefix = "archive-"
        with tempfile.TemporaryDirectory(
            delete=True,
            prefix=tmp_prefix,
        ) as tmp_dirname:
            with tempfile.NamedTemporaryFile(
                delete=True,
                suffix=f".{arch_suffix}",
                prefix=tmp_prefix,
            ) as tmp_arch:
                tmp_arch.write(archive)
                try:
                    patoolib.extract_archive(
                        tmp_arch.name,
                        outdir=tmp_dirname,
                        interactive=False,
                        password=password,
                        verbosity=True,
                    )
                except Exception as e:
                    log.warning(e)
                finally:
                    include_archive_exts = (
                        [] if recursive is False else include_archive_exts
                    )
                    for file_bytes, file_name in recursive_yield_file_bytes(
                        folder_path=tmp_dirname,
                        include_archive_exts=include_archive_exts,
                        include_document_exts=include_document_exts,
                    ):
                        yield file_bytes, file_name
