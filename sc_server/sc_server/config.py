import os
from typing import Dict
from dotenv import dotenv_values


class __Config:
    file_base: str = "/tmp/.sc_cache"

    model_path: str = "/tmp/.sc_cache/model.task"
    map_path: str = "/tmp/.sc_cache/map.json"

    command_queue_size: int = 10
    command_queue_timeout: int = 5

    reader_scanning_fps: float = 30.0
    reader_camera_id: int = 0

    recognizer_scanning_fps: float = 10.0

    filter_debounce_threshold: int = 2
    filter_short_threshold: int = 4
    filter_long_threshold: int = 8
    filter_long_interval: int = 10

    def __init__(self):
        _cfg: dict[str, str | None] = {**dotenv_values(".env"), **os.environ}
        self.__check_file(_cfg)
        self.__check_command(_cfg)
        self.__check_reader(_cfg)
        self.__check_recognizer(_cfg)
        self.__check_filter(_cfg)

    def __check_file(self, cfg: Dict[str, str | None]) -> None:
        _file_base = cfg.get("FILE_BASE")
        if _file_base is not None:
            self.file_base = _file_base

        if not os.path.isdir(self.file_base):
            os.makedirs(self.file_base)

        _model_path = cfg.get("MODEL_PATH")
        if _model_path is not None:
            self.model_path = _model_path

        _map_path = cfg.get("MAP_PATH")
        if _map_path is not None:
            self.map_path = _map_path

    def __check_command(self, cfg: Dict[str, str | None]) -> None:
        _command_queue_size = cfg.get("COMMAND_QUEUE_SIZE")
        if _command_queue_size is not None:
            self.command_queue_size = int(_command_queue_size)

        _command_queue_timeout = cfg.get("COMMAND_QUEUE_TIMEOUT")
        if _command_queue_timeout is not None:
            self.command_queue_timeout = int(_command_queue_timeout)

    def __check_reader(self, cfg: Dict[str, str | None]) -> None:
        _reader_scanning_fps = cfg.get("READER_SCANNING_FPS")
        if _reader_scanning_fps is not None:
            self.reader_scanning_fps = float(_reader_scanning_fps)

        _reader_camera_id = cfg.get("READER_CAMERA_ID")
        if _reader_camera_id is not None:
            self.reader_camera_id = int(_reader_camera_id)

    def __check_recognizer(self, cfg: Dict[str, str | None]) -> None:
        _recognizer_scanning_fps = cfg.get("RECOGNIZER_SCANNING_FPS")
        if _recognizer_scanning_fps is not None:
            self.recognizer_scanning_fps = float(_recognizer_scanning_fps)

    def __check_filter(self, cfg: Dict[str, str | None]) -> None:
        _filter_debounce_threshold = cfg.get("FILTER_DEBOUNCE_THRESHOLD")
        if _filter_debounce_threshold is not None:
            self.filter_debounce_threshold = int(_filter_debounce_threshold)

        _filter_short_threshold = cfg.get("FILTER_SHORT_THRESHOLD")
        if _filter_short_threshold is not None:
            self.filter_short_threshold = int(_filter_short_threshold)

        _filter_long_threshold = cfg.get("FILTER_LONG_THRESHOLD")
        if _filter_long_threshold is not None:
            self.filter_long_threshold = int(_filter_long_threshold)

        _filter_long_interval = cfg.get("FILTER_LONG_INTERVAL")
        if _filter_long_interval is not None:
            self.filter_long_interval = int(_filter_long_interval)


CONFIG = __Config()
