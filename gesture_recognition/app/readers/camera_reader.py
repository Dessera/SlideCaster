from typing import Any
from cv2 import VideoCapture
from cv2.typing import MatLike
from multiprocessing import Manager, Process

from . import ImageReader
from ..utils.fps_controller import fps_controller


class MultiProcessCameraReader(ImageReader):
    """利用多进程的摄像头读取器

    多进程用于对帧率进行转换，解决了 VideoCapture 类中内置的缓存机制导致的画面滞后问题。
    """

    __camera_id: int
    __fps: float
    __manager: Manager  # type: ignore
    __queue: Any
    __process: Process | None

    def __init__(self, camera_id: int = 0, fps: float = 30):
        self.__camera_id = camera_id
        self.__fps = fps
        self.__manager = Manager()
        self.__queue = self.__manager.Queue(maxsize=5)  # type: ignore

    @staticmethod
    def __read_process(camera_id: int, fps: float, queue: Any):
        camera = VideoCapture(camera_id)
        while camera.isOpened():
            with fps_controller(fps):
                ret, frame = camera.read()
                if not ret:
                    continue
                if queue.full():
                    queue.get()
                queue.put(frame)
        camera.release()

    def read(self) -> MatLike | None:
        if self.__queue.empty():
            return None
        frame = self.__queue.get()
        return frame

    def start(self):
        self.__process = Process(
            target=self.__read_process,
            args=(self.__camera_id, self.__fps, self.__queue),
        )
        self.__process.start()

    def stop(self):
        if self.__process is not None:
            self.__process.terminate()
            self.__process.join()
            self.__process = None


class CameraReader(ImageReader):
    """基础的摄像头读取器

    在测试时功能良好，但无法自定义帧率，VideoCapture 类中内置的缓存机制会导致捕获的画面在低帧率时严重滞后。
    """

    __camera: VideoCapture

    def __init__(self, camera_id: int = 0):
        self.__camera = VideoCapture(camera_id)
        # self.__camera.set(CAP_PROP_BUFFERSIZE, 1)

    def read(self) -> MatLike | None:
        ret, frame = self.__camera.read()
        if not ret:
            return None
        return frame
