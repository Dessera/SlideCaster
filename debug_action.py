import cv2
from hands_capture import HandsCapture
INIT_ENABLE_DEBUG = True
ENABLE_SETUP_HAND_MARK = True

'''
Class DebugAction is Majoring in Debugs Actions
involving:
browse the rt frame
see the hand marks
...
'''


class DebugAction:
    def __init__(self):
        self.enable_debug = INIT_ENABLE_DEBUG
        self.req_hands_cap = HandsCapture()
        self.enable_view_hand_marks = ENABLE_SETUP_HAND_MARK

    """
    To enable the process of find the marking points, Enabled the self.enable_debug by setting True
    Then set the self.enable_view_hand_marks true for accessing the hand marks
    """
    def mark_hands_feature(self, video_frame: cv2.Mat) -> cv2.Mat:
        if not self.enable_debug and not self.enable_view_hand_marks:
            return video_frame
        return self.req_hands_cap.get_marked_frame(video_frame)

    """
    To enable the process of show the RT frame, Enabled the self.enable_debug by setting True
    """
    def check_the_real_time_frame(self, video_frame: cv2.Mat, window_name="Debug Action: Frame Checker") -> None:
        if self.enable_debug:
            cv2.imshow(window_name, video_frame)
