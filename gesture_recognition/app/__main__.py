import asyncio

from .preprocessor.gesture_filter import GestureFilter

from .utils.fps_controller import async_fps_controller
from .recognizer.gesture_recognizer import GestureRecognizer
from .readers.camera_reader import MultiProcessCameraReader


async def main():
    reader = MultiProcessCameraReader()
    recognizer = GestureRecognizer()
    filter = GestureFilter()

    reader.start()

    while True:
        # take down the start time
        async with async_fps_controller(4):
            recognized_gesture = recognizer.recognize(reader)
            state, gesture = filter.filter(recognized_gesture)

            if gesture != "None" and state != "idle":
                print("Recognized gesture:", gesture, state)

    reader.stop()


asyncio.run(main())
