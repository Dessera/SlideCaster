import cv2
import mediapipe as mp

""" Configure """
SHELL_FLIP = True

"""
    Hands Features Capture
"""


class HandsCapture:
    MIN_DETECTION_CONFIDENCE = 0.75
    MIN_TRACKING_CONFIDENCE = 0.75
    STATIC_IMAGE_MODE = False
    MAX_NUM_HANDS = 2

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75)
        self.shell_flip = SHELL_FLIP

    def get_marked_frame(self, original_frame: cv2.Mat) -> cv2.Mat:
        frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
        if self.shell_flip:
            frame = cv2.flip(frame, 1)
        results = self.hands.process(frame)  # process()是手势识别最核心的方法，通过调用这个方法，将窗口对象作为参数，mediapipe就会将手势识别的信息存入到res对象中
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 关键点可视化
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame
