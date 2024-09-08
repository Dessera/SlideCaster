from dataclasses import dataclass

# TODO: 重构 GestureFilter 类，使其更加易读、易用


@dataclass
class GestureCache:
    gesture: str
    counter: int
    gesture_state: str
    short_gesture_triggered: bool


class GestureFilter:
    __current: GestureCache
    __next: GestureCache

    __debounce_threshold: int
    __short_threshold: int
    __long_threshold: int
    __long_interval: int

    def __init__(
        self,
        debounce_threshold: int = 2,
        short_threshold: int = 2,
        long_threshold: int = 10,
        long_interval: int = 5,
    ):
        self.__current = GestureCache("None", 0, "idle", False)
        self.__next = GestureCache("None", 0, "idle", False)

        self.__debounce_threshold = debounce_threshold
        self.__short_threshold = short_threshold
        self.__long_threshold = long_threshold
        self.__long_interval = long_interval

    def filter(self, gesture: str) -> tuple[str, str]:
        # 重置短按状态
        if self.__current.gesture_state == "short":
            self.__current.gesture_state = "idle"
        # 如果输入手势和当前手势相同 -> 操作延续
        if gesture == self.__current.gesture:
            self.__current.counter += 1

            # 如果手势计数器超过长阈值 -> 长按触发
            if self.__current.counter >= self.__long_threshold:
                # 每 long_interval 次长按触发一次
                if self.__current.counter % self.__long_interval == 0:
                    self.__current.gesture_state = "long"
                    self.__current.short_gesture_triggered = False
                else:
                    self.__current.gesture_state = "idle"
                # self.__current.gesture_state = "long"
                # self.__current.short_gesture_triggered = False
            # 如果手势计数器超过短阈值 -> 短按触发
            elif self.__current.counter >= self.__short_threshold:
                # 短按触发，防止重复触发
                if not self.__current.short_gesture_triggered:
                    self.__current.gesture_state = "short"
                    self.__current.short_gesture_triggered = True
            # 如果手势计数器未超过短阈值 -> 空闲
            else:
                self.__current.gesture_state = "idle"

        # 如果输入手势和当前手势不同 -> 消抖 -> 更新
        else:
            if self.__next.gesture == gesture:
                self.__next.counter += 1
                # 如果手势计数器超过阈值 -> 更新当前手势
                if self.__next.counter >= self.__debounce_threshold:
                    self.__current = self.__next
                    self.__next = GestureCache("None", 0, "idle", False)
            # 如果输入手势和下一个手势不同 -> 更新下一个手势
            else:
                self.__next = GestureCache(gesture, 1, "idle", False)

        return self.__current.gesture_state, self.__current.gesture
