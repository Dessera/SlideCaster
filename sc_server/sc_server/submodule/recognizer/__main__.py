# # import asyncio
# from typing import Any
# import requests
# from multiprocessing import Manager, Process
# from dataclasses import dataclass

# from .preprocessor.gesture_filter import GestureFilter
# from .utils.fps_controller import fps_controller
# from .recognizer.gesture_recognizer import GestureRecognizer
# from .readers.camera_reader import MultiProcessCameraReader
# from .config import Config

# # TODO: 待封装


# @dataclass
# class Gesture:
#     label: str
#     operation: str


# manager = Manager()
# # queue: asyncio.Queue[Gesture] = asyncio.Queue()
# queue = manager.Queue()
# config = Config()


# def create_subprocess():
#     p = Process(target=gesture_sender, args=(queue,))
#     p.start()
#     return p


# def destroy_subprocess(p: Process):
#     p.terminate()
#     p.join()


# def gesture_sender(que: Any):
#     while True:
#         try:
#             g_operation = que.get()
#             r = requests.post(  # type: ignore
#                 url=f"{config.controller_center_url}",
#                 json={"label": g_operation.label, "operation": g_operation.operation},
#             )
#             print(f"Sent gesture: {g_operation}, status code: {r.status_code}")  # type: ignore
#         except Exception as e:
#             print(f"Error: {e}")


# def main():
#     reader = MultiProcessCameraReader(
#         camera_id=config.reader_camera_id,
#         fps=config.reader_scanning_fps,
#     )
#     recognizer = GestureRecognizer(
#         model_path=config.recognizer_model_path,
#     )
#     filter = GestureFilter(
#         debounce_threshold=config.filter_debounce_threshold,
#         short_threshold=config.filter_short_threshold,
#         long_threshold=config.filter_long_threshold,
#         long_interval=config.filter_long_interval,
#     )
#     sub_process = create_subprocess()
#     reader.start()

#     while True:
#         # take down the start time
#         with fps_controller(config.recognizer_scanning_fps):
#             recognized_gesture = recognizer.recognize(reader)
#             state, gesture = filter.filter(recognized_gesture)

#             if gesture != "None" and state != "idle":
#                 queue.put(Gesture(gesture, state))

#     reader.stop()
#     destroy_subprocess(sub_process)


# main()
