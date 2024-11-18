import os
from typing import Dict
from dotenv import dotenv_values


class __Config:
    file_base: str

    def __init__(self):
        _cfg: dict[str, str | None] = {**dotenv_values(".env"), **os.environ}
        self.__check_file(_cfg)

    def __check_file(self, cfg: Dict[str, str | None]) -> None:
        _file_base = cfg.get("FILE_BASE")
        if _file_base is None:
            _file_base = "/tmp/.sc_cache"

        if not os.path.isdir(_file_base):
            os.makedirs(_file_base)

        self.file_base = _file_base


CONFIG = __Config()
