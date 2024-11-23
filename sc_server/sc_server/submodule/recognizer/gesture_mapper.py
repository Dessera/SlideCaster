import json

from typing import Dict


class GestureMapper:
    m_map: Dict[str, Dict[str, str]]

    def __init__(self, map_path: str):
        self.load_map(map_path)

    def load_map(self, map_path: str):
        with open(map_path, "r") as f:
            self.m_map = json.load(f)

    def map(self, gesture: str, state: str) -> str | None:
        return self.m_map.get(gesture, {}).get(state, None)
