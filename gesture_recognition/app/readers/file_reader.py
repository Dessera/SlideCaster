from . import ImageReader
from cv2 import imread
from cv2.typing import MatLike


class FileReader(ImageReader):
    __path: str

    def __init__(self, path: str):
        self.__path = path

    def read(self) -> MatLike | None:
        try:
            frame = imread(self.__path)
            return frame
        except Exception:
            return None
