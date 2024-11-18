import os
from typing import Dict
from dotenv import dotenv_values


class __Config:
    file_base: str = "/tmp/.sc_cache"

    command_queue_size: int = 10
    command_queue_timeout: int = 5

    def __init__(self):
        _cfg: dict[str, str | None] = {**dotenv_values(".env"), **os.environ}
        self.__check_file(_cfg)
        self.__check_command(_cfg)

    def __check_file(self, cfg: Dict[str, str | None]) -> None:
        _file_base = cfg.get("FILE_BASE")
        if _file_base is not None:
            self.file_base = _file_base

        if not os.path.isdir(self.file_base):
            os.makedirs(self.file_base)

    def __check_command(self, cfg: Dict[str, str | None]) -> None:
        _command_queue_size = cfg.get("COMMAND_QUEUE_SIZE")
        if _command_queue_size is not None:
            self.command_queue_size = int(_command_queue_size)

        _command_queue_timeout = cfg.get("COMMAND_QUEUE_TIMEOUT")
        if _command_queue_timeout is not None:
            self.command_queue_timeout = int(_command_queue_timeout)


CONFIG = __Config()
