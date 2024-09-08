from dotenv import dotenv_values


class Config:
    reader_scanning_fps: float
    reader_camera_id: int

    recognizer_scanning_fps: float
    recognizer_model_path: str

    filter_debounce_threshold: int
    filter_short_threshold: int
    filter_long_threshold: int
    filter_long_interval: int

    controller_center_url: str

    def __init__(self):
        _cfg = dotenv_values(".env")
        self.check_reader(_cfg)
        self.check_recognizer(_cfg)
        self.check_filter(_cfg)
        self.check_controller(_cfg)

    def check_reader(self, _cfg: dict[str, str | None]):
        assert "READER_SCANNING_FPS" in _cfg, "READER_SCANNING_FPS is required"
        if _cfg["READER_SCANNING_FPS"] is None:
            raise ValueError("READER_SCANNING_FPS is required")
        self.reader_scanning_fps = float(_cfg["READER_SCANNING_FPS"])

        assert "READER_CAMERA_ID" in _cfg, "READER_CAMERA_ID is required"
        if _cfg["READER_CAMERA_ID"] is None:
            raise ValueError("READER_CAMERA_ID is required")
        self.reader_camera_id = int(_cfg["READER_CAMERA_ID"])

    def check_recognizer(self, _cfg: dict[str, str | None]):
        assert "RECOGNIZER_SCANNING_FPS" in _cfg, "RECOGNIZER_SCANNING_FPS is required"
        if _cfg["RECOGNIZER_SCANNING_FPS"] is None:
            raise ValueError("RECOGNIZER_SCANNING_FPS is required")
        self.recognizer_scanning_fps = float(_cfg["RECOGNIZER_SCANNING_FPS"])

        assert "RECOGNIZER_MODEL_PATH" in _cfg, "RECOGNIZER_MODEL_PATH is required"
        if _cfg["RECOGNIZER_MODEL_PATH"] is None:
            raise ValueError("RECOGNIZER_MODEL_PATH is required")
        self.recognizer_model_path = _cfg["RECOGNIZER_MODEL_PATH"]

    def check_filter(self, _cfg: dict[str, str | None]):
        assert (
            "FILTER_DEBOUNCE_THRESHOLD" in _cfg
        ), "FILTER_DEBOUNCE_THRESHOLD is required"
        if _cfg["FILTER_DEBOUNCE_THRESHOLD"] is None:
            raise ValueError("FILTER_DEBOUNCE_THRESHOLD is required")
        self.filter_debounce_threshold = int(_cfg["FILTER_DEBOUNCE_THRESHOLD"])

        assert "FILTER_SHORT_THRESHOLD" in _cfg, "FILTER_SHORT_THRESHOLD is required"
        if _cfg["FILTER_SHORT_THRESHOLD"] is None:
            raise ValueError("FILTER_SHORT_THRESHOLD is required")
        self.filter_short_threshold = int(_cfg["FILTER_SHORT_THRESHOLD"])

        assert "FILTER_LONG_THRESHOLD" in _cfg, "FILTER_LONG_THRESHOLD is required"
        if _cfg["FILTER_LONG_THRESHOLD"] is None:
            raise ValueError("FILTER_LONG_THRESHOLD is required")
        self.filter_long_threshold = int(_cfg["FILTER_LONG_THRESHOLD"])

        assert "FILTER_LONG_INTERVAL" in _cfg, "FILTER_LONG_INTERVAL is required"
        if _cfg["FILTER_LONG_INTERVAL"] is None:
            raise ValueError("FILTER_LONG_INTERVAL is required")
        self.filter_long_interval = int(_cfg["FILTER_LONG_INTERVAL"])

    def check_controller(self, _cfg: dict[str, str | None]):
        assert "CONTROLLER_CENTER_URL" in _cfg, "CONTROLLER_CENTER_URL is required"
        if _cfg["CONTROLLER_CENTER_URL"] is None:
            raise ValueError("CONTROLLER_CENTER_URL is required")
        self.controller_center_url = _cfg["CONTROLLER_CENTER_URL"]
