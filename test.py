from gesture_recognitions import GestureRecognition
from result_handler import GestureRecognizerResultAnalyzer
from debug_action import DebugAction
import cv2

# Create Video capture instance to cap from default camera
cap = cv2.VideoCapture(0)
# Create Gesture Analyzer
gesture_recognizer = GestureRecognition()
debug_action = DebugAction()
# We do start an infinite loop
# UNTIL the camera is unacceptable or user himself interrupt
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # fetch the result from the frame
    result = gesture_recognizer.get_from_cv_image(frame)
    # Check the availability of the result
    if GestureRecognizerResultAnalyzer.check_result_available(result):
        # Get the type
        gesture_type = GestureRecognizerResultAnalyzer.get_gesture_signals(result)
        print(gesture_type)
    # Display the frame
    # See debug action for settings
    frame = debug_action.mark_hands_feature(frame)
    debug_action.check_the_real_time_frame(frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

