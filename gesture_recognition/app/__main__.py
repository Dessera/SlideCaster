import asyncio
import requests
from dataclasses import dataclass

from .preprocessor.gesture_filter import GestureFilter
from .utils.fps_controller import async_fps_controller
from .recognizer.gesture_recognizer import GestureRecognizer
from .readers.camera_reader import MultiProcessCameraReader
from .config import Config

# TODO: 待封装


@dataclass
class Gesture:
    label: str
    operation: str


queue: asyncio.Queue[Gesture] = asyncio.Queue()
config = Config()


async def gesture_sender():
    while True:
        try:
            g_operation = await queue.get()
            r = requests.post(  # type: ignore
                url=f"{config.controller_center_url}",
                json={"label": g_operation.label, "operation": g_operation.operation},
            )
            print(f"Sent gesture: {g_operation}, status code: {r.status_code}")  # type: ignore
            queue.task_done()
        except Exception as e:
            print(f"Error: {e}")


async def main():
    reader = MultiProcessCameraReader(
        camera_id=config.reader_camera_id,
        fps=config.reader_scanning_fps,
    )
    recognizer = GestureRecognizer(
        model_path=config.recognizer_model_path,
    )
    filter = GestureFilter(
        debounce_threshold=config.filter_debounce_threshold,
        short_threshold=config.filter_short_threshold,
        long_threshold=config.filter_long_threshold,
        long_interval=config.filter_long_interval,
    )

    reader.start()

    while True:
        # take down the start time
        async with async_fps_controller(config.recognizer_scanning_fps):
            recognized_gesture = recognizer.recognize(reader)
            state, gesture = filter.filter(recognized_gesture)

            if gesture != "None" and state != "idle":
                await queue.put(Gesture(gesture, state))

    reader.stop()


loop = asyncio.get_event_loop()
loop.create_task(gesture_sender())
loop.create_task(main())
loop.run_forever()
