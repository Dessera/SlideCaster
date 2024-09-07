from . import ImageReader
from cv2 import imread, Mat


class FileReader(ImageReader):
    __path: str

    def __init__(self, path: str):
        self.__path = path

    def read(self) -> Mat | None:
        try:
            frame = imread(self.__path)
            return Mat(frame)
        except Exception:
            return None
