import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from image_factory import MpImageFactory


class GestureRecognition:
    def __init__(self):
        self.recognizer = None
        self.__init_default_recognizer()

    """
        INIT the recognizer as default, usually use the default recognizers
    """

    def __init_default_recognizer(self):
        # Defaultly, we use the default recognizer
        base_options = python.BaseOptions(
            model_asset_path="models/default/default_gesture_recognizer.task"
        )
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def switch_model(self, model_path: str):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    """
        Core Implements of recognize gestures from general Image
    """

    def __recognize_gesture_impl(self, target_image: mp.Image):
        recognition_result = self.recognizer.recognize(target_image)
        return recognition_result

    """
        do recognize from available cv image
    """

    def get_from_cv_image(self, cv_image: cv2.Mat):
        return self.__recognize_gesture_impl(
            MpImageFactory.convert_from_cv_color_image(cv_image=cv_image)
        )

    """
        do recognize from available file path
    """

    def get_from_file_name(self, file_path: str):
        return self.__recognize_gesture_impl(
            MpImageFactory.convert_from_file_path(image_path=file_path)
        )
