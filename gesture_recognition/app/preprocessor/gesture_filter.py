# GestureFilter 为了对手势序列进行过滤，将手势序列中的噪声数据去除
# 手势序列每隔半秒读取一次，而这个类的目的就是将手势序列处理为实际的控制手势
# 例如，在实际操作中，有短手势和长手势两种类型
# 短手势：手势持续时间在1-2秒之间
# 长手势：手势持续时间在2秒以上
# 现在，我们输入一个手势序列，例如：[
#     "Thumb up",
#     "Thumb up",
#     "Thumb up",
#     "Thumb up",
#     "Thumb up",
# ]
# 这个序列中有5个"Thumb up"，我们认为这是一个长手势，但在实际操作中，我们无法预知这个手势序列的长度
# 所以我们需要一个类来处理这个问题，应用有限状态机的思想，将手势序列处理为实际的控制手势


class GestureFilter:
    __state: str
    __count: int
    __gesture: str

    def __init__(self):
        self.__state = "idle"
        self.__count = 0
        self.__gesture = ""

    def filter(self, gesture: str) -> str | None:
        if gesture == self.__gesture:
            self.__count += 1
        else:
            self.__count = 1
            self.__gesture = gesture

        if self.__count >= 5:
            if self.__state == "idle":
                self.__state = "short"
            elif self.__state == "short":
                self.__state = "long"
            elif self.__state == "long":
                self.__state = "long"
        else:
            self.__state = "idle"

        if self.__state == "short":
            return self.__gesture
        elif self.__state == "long":
            return self.__gesture
        else:
            return None
