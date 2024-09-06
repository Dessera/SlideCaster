from mediapipe import Image, ImageFormat  # type: ignore
import cv2


class MpImageFactory:
    @staticmethod
    def convert_from_cv_color_image(cv_image: cv2.Mat) -> Image:  # type: ignore
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)  # type: ignore
        return Image(image_format=ImageFormat.SRGB, data=cv_image)  # type: ignore

    @staticmethod
    def convert_from_file_path(image_path) -> Image:  # type: ignore
        return Image.create_from_file(image_path)  # type: ignore
