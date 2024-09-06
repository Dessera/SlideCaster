from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizerResult


class GestureRecognizerResultAnalyzer:
    """
    This method aims t check whether the result is worth handle
    True: can be further process by get_gesture_signals(which is at below)
    """

    @staticmethod
    def check_result_available(result: GestureRecognizerResult) -> bool:
        return len(result.gestures) != 0

    """
    Process with fetching the results
    shell get the gesture name directly
    """
    @staticmethod
    def get_gesture_signals(result: GestureRecognizerResult) -> str:
        return result.gestures[0][0].category_name
