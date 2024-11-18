import os
import time

from ..config import CONFIG


def is_pdf_file(file_name: str) -> bool:
    return os.path.isfile(file_name) and file_name.endswith(".pdf")


def get_full_path(file_name: str):
    return os.path.join(CONFIG.file_base, file_name)


def get_default_filename():
    currtm = time.time_ns()
    return f"{currtm}.pdf"


def get_files():
    entries = os.listdir(CONFIG.file_base)
    return list(filter(lambda e: is_pdf_file(get_full_path(e)), entries))


def get_file(file_name: str):
    full_path = get_full_path(file_name)
    if not is_pdf_file(full_path):
        return None
    return full_path


def save_file(file_content: bytes, file_name: str | None = None):
    if file_name is None:
        file_name = get_default_filename()
    full_path = get_full_path(file_name)
    with open(full_path, "wb") as f:
        f.write(file_content)
    return full_path


def delete_file(file_name: str):
    full_path = get_full_path(file_name)
    if not is_pdf_file(full_path):
        return False
    os.remove(full_path)
    return True
