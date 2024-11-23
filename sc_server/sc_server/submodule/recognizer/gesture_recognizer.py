from typing import Any
from cv2 import cvtColor, COLOR_BGR2RGB
from cv2.typing import MatLike
from mediapipe.tasks.python.vision.gesture_recognizer import (
    GestureRecognizerResult,
    GestureRecognizerOptions,
    GestureRecognizer as GestureRecognizerImpl,
)
from mediapipe.tasks.python.core.base_options import BaseOptions as ModelBaseOptions
from mediapipe import Image, ImageFormat  # type: ignore


class GestureRecognizer:
    m_recognizer: GestureRecognizerImpl

    def __init__(self, model_path: str):
        self.switch_model(model_path)

    @staticmethod
    def __from_cv_color_image(cv_image: MatLike) -> Image:  # type: ignore
        cv_image_conv = cvtColor(cv_image, COLOR_BGR2RGB)  # type: ignore
        return Image(image_format=ImageFormat.SRGB, data=cv_image_conv)  # type: ignore

    def __recognize_impl(self, image: Image) -> GestureRecognizerResult:  # type: ignore
        return self.m_recognizer.recognize(image)  # type: ignore

    def switch_model(self, model_path: str):
        base_options = ModelBaseOptions(model_asset_path=model_path)
        options = GestureRecognizerOptions(base_options=base_options)
        self.m_recognizer = GestureRecognizerImpl.create_from_options(options)

    def recognize(self, cv_image: Any) -> str:
        if cv_image is None:
            return "None"
        image = self.__from_cv_color_image(cv_image)  # type: ignore
        result = self.__recognize_impl(image)  # type: ignore
        if len(result.gestures) == 0:  # type: ignore
            return "None"
        return result.gestures[0][0].category_name  # type: ignore
