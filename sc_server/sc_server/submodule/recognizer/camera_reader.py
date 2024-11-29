import multiprocessing as mp
import signal
import sys

from cv2 import VideoCapture
from cv2.typing import MatLike


from ...utils.fps_controller import fps_controller


def _read_process_handler(camera_id: int, fps: float, queue: mp.Queue):
    camera = VideoCapture(camera_id)

    # handle sigterm
    def exit_handler(signum, frame):
        camera.release()
        sys.exit(0)

    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)

    # Ensure no exception is raised when camera is not opened
    # just for robustness :)
    while True:
        with fps_controller(fps):
            ret, frame = camera.read()
            if not ret:
                continue
            # Queue is full, drop the oldest frame
            if queue.full():
                queue.get()
            queue.put(frame)


class MultiProcessCameraReader:
    """利用多进程的摄像头读取器

    多进程用于对帧率进行转换，解决了 VideoCapture 类中内置的缓存机制导致的画面滞后问题。
    """

    m_camera_id: int
    m_fps: float
    m_queue = mp.Queue(maxsize=5)
    m_process: mp.Process | None

    def __init__(self, camera_id: int = 0, fps: float = 30):
        self.m_camera_id = camera_id
        self.m_fps = fps

    def read(self) -> MatLike | None:
        if self.m_queue.empty():
            return None
        frame = self.m_queue.get()
        return frame

    def start(self):
        self.m_process = mp.Process(
            target=_read_process_handler,
            args=(self.m_camera_id, self.m_fps, self.m_queue),
        )
        self.m_process.start()

    def stop(self, timeout: float | None = None):
        if self.m_process is not None:
            self.m_process.terminate()
            self.m_process.join(timeout)
            self.m_process = None
