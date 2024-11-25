import os
import time

from ..config import CONFIG
from ..utils.singleton import singleton


@singleton
class FileService:
    def is_pdf_file(self, file_name: str) -> bool:
        return os.path.isfile(file_name) and file_name.endswith(".pdf")

    def get_full_path(self, file_name: str):
        return os.path.join(CONFIG.file_base, file_name)

    def get_default_filename(self):
        currtm = time.time_ns()
        return f"{currtm}.pdf"

    def get_files(self):
        entries = os.listdir(CONFIG.file_base)
        return list(filter(lambda e: self.is_pdf_file(self.get_full_path(e)), entries))

    def get_file(self, file_name: str):
        full_path = self.get_full_path(file_name)
        if not self.is_pdf_file(full_path):
            return None
        return full_path

    def save_file(self, file_content: bytes, file_name: str | None = None):
        if file_name is None:
            file_name = self.get_default_filename()
        full_path = self.get_full_path(file_name)
        with open(full_path, "wb") as f:
            f.write(file_content)
        return full_path

    def delete_file(self, file_name: str):
        full_path = self.get_full_path(file_name)
        if not self.is_pdf_file(full_path):
            return False
        os.remove(full_path)
        return True
