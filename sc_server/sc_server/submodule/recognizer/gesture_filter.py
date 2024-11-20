from dataclasses import dataclass


@dataclass
class GestureCache:
    g_label: str = "None"
    cnt: int = 0
    g_state: str = "idle"
    s_trig: bool = False


class GestureFilter:
    _current: GestureCache = GestureCache()
    _next: GestureCache = GestureCache()

    m_dthres: int
    m_sthres: int
    m_lthres: int
    m_linterval: int

    def __init__(
        self,
        debounce_threshold: int = 2,
        short_threshold: int = 2,
        long_threshold: int = 10,
        long_interval: int = 5,
    ):
        self.m_dthres = debounce_threshold
        self.m_sthres = short_threshold
        self.m_lthres = long_threshold
        self.m_linterval = long_interval

    def filter(self, gesture: str) -> tuple[str, str]:
        # 重置短按状态
        if self._current.g_state == "short":
            self._current.g_state = "idle"
        # 如果输入手势和当前手势相同 -> 操作延续
        if gesture == self._current.g_label:
            self._current.cnt += 1

            # 如果手势计数器超过长阈值 -> 长按触发
            if self._current.cnt >= self.m_lthres:
                # 每 long_interval 次长按触发一次
                if self._current.cnt % self.m_linterval == 0:
                    self._current.g_state = "long"
                    self._current.s_trig = False
                else:
                    self._current.g_state = "idle"
                # self.__current.gesture_state = "long"
                # self.__current.short_gesture_triggered = False
            # 如果手势计数器超过短阈值 -> 短按触发
            elif self._current.cnt >= self.m_sthres:
                # 短按触发，防止重复触发
                if not self._current.s_trig:
                    self._current.g_state = "short"
                    self._current.s_trig = True
            # 如果手势计数器未超过短阈值 -> 空闲
            else:
                self._current.g_state = "idle"

        # 如果输入手势和当前手势不同 -> 消抖 -> 更新
        else:
            if self._next.g_label == gesture:
                self._next.cnt += 1
                # 如果手势计数器超过阈值 -> 更新当前手势
                if self._next.cnt >= self.m_dthres:
                    self._current = self._next
                    self._next = GestureCache()
            # 如果输入手势和下一个手势不同 -> 更新下一个手势
            else:
                self._next = GestureCache(gesture, 1)

        return self._current.g_state, self._current.g_label
