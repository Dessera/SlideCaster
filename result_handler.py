from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizerResult


class GestureRecognizerResultAnalyzer:
    @staticmethod
    def check_result_available(result: GestureRecognizerResult) -> bool:
        return len(result.gestures) != 0

    @staticmethod
    def get_gesture_signals(result: GestureRecognizerResult) -> str:
        return result.gestures[0][0].category_name
