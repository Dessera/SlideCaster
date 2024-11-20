import json
from typing import Dict
from multiprocessing import Queue

from .camera_reader import MultiProcessCameraReader
from .gesture_recognizer import GestureRecognizer
from .gesture_filter import GestureFilter
from .utils.fps_controller import fps_controller

from ...config import CONFIG


class SCClient:
    m_reader: MultiProcessCameraReader
    m_recognizer: GestureRecognizer
    m_filter: GestureFilter

    m_map: Dict[str, Dict[str, str]]

    def _init_mapper(self):
        try:
            with open(CONFIG.map_path, "r") as f:
                self.m_map = json.load(f)
        except FileNotFoundError:
            self.m_map = {}

    def _map_command(self, gesture: str, state: str) -> str:
        return self.m_map.get(gesture, {}).get(state, "None")

    def __init__(self) -> None:
        self.m_reader = MultiProcessCameraReader(
            camera_id=CONFIG.reader_camera_id, fps=CONFIG.reader_scanning_fps
        )
        self.m_recognizer = GestureRecognizer(model_path=CONFIG.model_path)
        self.m_filter = GestureFilter(
            debounce_threshold=CONFIG.filter_debounce_threshold,
            short_threshold=CONFIG.filter_short_threshold,
            long_threshold=CONFIG.filter_long_threshold,
            long_interval=CONFIG.filter_long_interval,
        )

        self._init_mapper()

    def run(self, queue: Queue):
        try:
            self.m_reader.start()

            while True:
                with fps_controller(CONFIG.recognizer_scanning_fps):
                    cv_img = self.m_reader.read()
                    gst = self.m_recognizer.recognize(cv_img)

                    state, gesture = self.m_filter.filter(gst)
                    command = self._map_command(gesture, state)

                    if command != "None" and gesture != "None" and state != "idle":
                        queue.put(command)

        except Exception:
            pass
        finally:
            self.m_reader.stop()


def entry(queue: Queue):
    client = SCClient()
    client.run(queue)
