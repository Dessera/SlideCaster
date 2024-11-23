from dataclasses import dataclass


@dataclass
class GestureCache:
    g_label: str = "None"
    cnt: int = 0
    g_state: str = "idle"
    s_trig: bool = False


# Module to filter gestures
# bullshit fsm, but I have no idea either :(
class GestureFilter:
    m_current: GestureCache = GestureCache()
    m_next: GestureCache = GestureCache()

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
        if self.m_current.g_state == "short":
            self.m_current.g_state = "idle"
        # 如果输入手势和当前手势相同 -> 操作延续
        if gesture == self.m_current.g_label:
            self.m_current.cnt += 1

            # 如果手势计数器超过长阈值 -> 长按触发
            if self.m_current.cnt >= self.m_lthres:
                # 每 long_interval 次长按触发一次
                if self.m_current.cnt % self.m_linterval == 0:
                    self.m_current.g_state = "long"
                    self.m_current.s_trig = False
                else:
                    self.m_current.g_state = "idle"
            # 如果手势计数器超过短阈值 -> 短按触发
            elif self.m_current.cnt >= self.m_sthres:
                # 短按触发，防止重复触发
                if not self.m_current.s_trig:
                    self.m_current.g_state = "short"
                    self.m_current.s_trig = True
            # 如果手势计数器未超过短阈值 -> 空闲
            else:
                self.m_current.g_state = "idle"

        # 如果输入手势和当前手势不同 -> 消抖 -> 更新
        else:
            if self.m_next.g_label == gesture:
                self.m_next.cnt += 1
                # 如果手势计数器超过阈值 -> 更新当前手势
                if self.m_next.cnt >= self.m_dthres:
                    self.m_current = self.m_next
                    self.m_next = GestureCache()
            # 如果输入手势和下一个手势不同 -> 更新下一个手势
            else:
                self.m_next = GestureCache(gesture, 1)

        return self.m_current.g_state, self.m_current.g_label
