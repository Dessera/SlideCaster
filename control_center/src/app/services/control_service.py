import asyncio
from asyncio import Queue

from ..utils.singleton import singleton  # type: ignore
from ..models.control_model import (
    Command,
    Gesture,
    GestureLabel,
    GestureOperation,
    GestureParsedError,
)


@singleton
class ControlService:
    __queue: Queue[Command]
    __timeout: int

    # 手势和操作指令的映射关系
    __gesture_to_command: dict[GestureLabel, dict[GestureOperation, Command]] = {
        "Thumb_Up": {"short": "page:prev", "long": "page:prev"},
        "Thumb_Down": {"short": "page:next", "long": "page:next"},
        "Open_Palm": {"short": "scale:up", "long": "scale:up"},
        "Closed_Fist": {"short": "scale:down", "long": "scale:down"},
    }

    def __init__(self):
        self.__timeout = 5
        self.__queue = Queue(maxsize=5)

    async def put(self, operation: Command):
        """操作队列的put方法，当延迟超过一定时间后，该操作就不再有效，因此需要设置超时时间

        Args:
            operation (str): 操作指令
        """
        await asyncio.wait_for(self.__queue.put(operation), timeout=self.__timeout)

    async def get(self) -> Command:
        """操作队列的get方法，因为消费者必须准确的执行任何队列中的操作，所以不能设置超时时间

        Returns:
            str: 操作指令
        """
        return await self.__queue.get()

    def parse(self, gesture: Gesture) -> Command:
        """解析手势操作

        Args:
            gesture (Gesture): 手势操作

        Returns:
            str: 操作指令
        """
        operation_map = self.__gesture_to_command.get(gesture.label)
        if operation_map is None:
            raise GestureParsedError(gesture)
        command = operation_map.get(gesture.operation)
        if command is None:
            raise GestureParsedError(gesture)
        return command
