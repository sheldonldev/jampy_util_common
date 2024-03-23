import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import magic
import patoolib  # type: ignore

from ._log import log
from .path import ARCHIVE_EXTS, DOCUMENT_EXTS, IGNORE_NAMES, FileExtension


def json_to_bytes(
    json_: Dict | List[Dict], intent=4, ensure_ascii=False, encoding="utf-8"
) -> bytes:
    return bytes(
        json.dumps(json_, indent=intent, ensure_ascii=ensure_ascii),
        encoding=encoding,
    )


def str_to_bytes(text: str, encoding="utf-8") -> bytes:
    return bytes(text, encoding=encoding)


def guess_file_extension(file: bytes) -> Optional[str]:
    # TODO: 如果结果与实际不符，需要进一步更正。
    # 用libreoffice 查看media-type:
    # https://wiki.documentfoundation.org/Macros/Python_Guide/Introduction

    mime = magic.from_buffer(file, mime=True).lower()

    if "zip" in mime:
        return FileExtension.ZIP.value

    if "rar" in mime:
        return FileExtension.RAR.value

    if "7z" in mime:
        return FileExtension._7Z.value

    if "word" in mime and "document" not in mime:
        return FileExtension.DOC.value

    if "word" in mime and "document" in mime:
        return FileExtension.DOCX.value

    if "excel" in mime:
        return FileExtension.XLS.value

    if "sheet" in mime:
        return FileExtension.XLSX.value

    if "jpeg" in mime or "jpg" in mime:
        return FileExtension.JPG.value

    if "png" in mime:
        return FileExtension.PNG.value

    if "pdf" in mime:
        return FileExtension.PDF.value

    return None


def recursive_yield_file_bytes(
    folder_path,
    include_archive_exts: List[str] = ARCHIVE_EXTS,
    include_document_exts: List[str] = DOCUMENT_EXTS,
) -> Iterable[Tuple[bytes, str]]:
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
            if ext in include_document_exts:
                yield file_bytes, ext

            if ext in include_archive_exts:
                for bytes_ext_pair in yield_files_from_archive(
                    file_bytes,
                    ext,
                    include_archive_exts=include_archive_exts,
                    include_document_exts=include_document_exts,
                    recursive=True,
                ):
                    yield bytes_ext_pair


def yield_files_from_archive(
    archive: bytes,
    password: Optional[str] = None,
    include_archive_exts: List[str] = ARCHIVE_EXTS,
    include_document_exts: List[str] = DOCUMENT_EXTS,
    recursive: bool = False,
) -> Iterable[Tuple[bytes, str]]:
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
            # outdir = Path(tmp_dirname).joinpath(format_now())
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
                    for bytes_ext_pair in recursive_yield_file_bytes(
                        folder_path=tmp_dirname,
                        include_archive_exts=include_archive_exts,
                        include_document_exts=include_document_exts,
                    ):
                        yield bytes_ext_pair
