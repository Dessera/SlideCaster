from abc import ABCMeta, abstractmethod
from typing import Any

from ..readers import ImageReader


class BasicRecognizer(metaclass=ABCMeta):
    """不可继承的基础识别器类"""

    @abstractmethod
    def recognize(self, reader: Any) -> str:
        pass


class ImageRecognizer(BasicRecognizer):

    @abstractmethod
    def recognize(self, reader: ImageReader) -> str:
        pass
