import asyncio

from .utils.fps_controller import async_fps_controller
from .recognizer.gesture_recognizer import GestureRecognizer
from .readers.camera_reader import MultiProcessCameraReader

# RECOGNIZE_INTERVAL_MS = 1000


async def main():
    reader = MultiProcessCameraReader()
    recognizer = GestureRecognizer()

    reader.start()

    while True:
        # take down the start time
        async with async_fps_controller(2):
            recognized_gesture = recognizer.recognize(reader)
            if recognized_gesture is not None:
                print("Recognized gesture:", recognized_gesture)
            else:
                print("No gesture recognized")

    reader.stop()


asyncio.run(main())
