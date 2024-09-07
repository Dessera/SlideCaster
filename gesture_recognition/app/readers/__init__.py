from abc import ABCMeta, abstractmethod
from typing import Any
from cv2.typing import MatLike


class BasicReader(metaclass=ABCMeta):

    @abstractmethod
    def read(self) -> Any:
        pass


class ImageReader(BasicReader):

    @abstractmethod
    def read(self) -> MatLike | None:
        pass


class TextReader(BasicReader):

    @abstractmethod
    def read(self) -> str | None:
        pass
