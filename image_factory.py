from mediapipe import Image, ImageFormat
import cv2

# Image Factory:> wrap the image convertion
class MpImageFactory:
    @staticmethod
    def convert_from_cv_color_image(cv_image: cv2.Mat) -> Image:
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        return Image(image_format=ImageFormat.SRGB, data=cv_image)

    @staticmethod
    def convert_from_file_path(image_path) -> Image:
        return Image.create_from_file(image_path)
