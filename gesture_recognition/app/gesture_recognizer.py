import cv2
from mediapipe.tasks.python.vision.gesture_recognizer import (
    GestureRecognizerResult,
    GestureRecognizerOptions,
    GestureRecognizer as GestureRecognizerImpl,
)
from mediapipe.tasks.python.core.base_options import BaseOptions as ModelBaseOptions
import mediapipe as mp

from .mp_image_factory import MpImageFactory


class GestureRecognizer:

    recognizer: GestureRecognizerImpl = None  # type: ignore

    def __init__(self):
        self.switch_model("models/default/default_gesture_recognizer.task")

    def switch_model(self, model_path: str):
        """切换模型（加载新的模型）

        Args:
            model_path (str): 模型路径
        """
        base_options = ModelBaseOptions(model_asset_path=model_path)
        options = GestureRecognizerOptions(base_options=base_options)
        self.recognizer = GestureRecognizerImpl.create_from_options(options)

    def __recognize_impl(self, image: mp.Image) -> GestureRecognizerResult:  # type: ignore
      """识别手势的实现函数

      Args:
          image (mp.Image): 输入图像，类型来自mediapipe

      Returns:
          GestureRecognizerResult: 识别结果
      """
        return self.recognizer.recognize(image)  # type: ignore
      
    def recognize_from_cv_image(self, cv_image: cv2.Mat) -> GestureRecognizerResult:
        """从OpenCV图像中识别手势

        Args:
            cv_image ([cv2.Mat]): OpenCV图像

        Returns:
            GestureRecognizerResult: 识别结果
        """
        image = MpImageFactory.convert_from_cv_color_image(cv_image) # type: ignore
        return self.__recognize_impl(image) # type: ignore

    def recognize_from_file_path(self, image_path: str) -> GestureRecognizerResult:
        """从文件中识别手势

        Args:
            image_path (str): 图像路径

        Returns:
            GestureRecognizerResult: 识别结果
        """
        image = MpImageFactory.convert_from_file_path(image_path) # type: ignore
        return self.__recognize_impl(image) # type: ignore