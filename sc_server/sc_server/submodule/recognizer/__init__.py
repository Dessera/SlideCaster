import logging
import signal
import sys
from multiprocessing import Queue

from .camera_reader import MultiProcessCameraReader
from .gesture_recognizer import GestureRecognizer
from .gesture_filter import GestureFilter
from .gesture_mapper import GestureMapper
from ...utils.fps_controller import fps_controller

from ...config import CONFIG


def entry(queue: Queue):
    logging.basicConfig(level=CONFIG.log_level)
    logger = logging.getLogger("gesture_recognizer")

    logger.info("gesture recognizer initializing")

    # early initialization (disallow any exceptions)
    try:
        recognizer = GestureRecognizer(model_path=CONFIG.model_path)
        filter = GestureFilter(
            debounce_threshold=CONFIG.filter_debounce_threshold,
            short_threshold=CONFIG.filter_short_threshold,
            long_threshold=CONFIG.filter_long_threshold,
            long_interval=CONFIG.filter_long_interval,
        )
        mapper = GestureMapper(CONFIG.map_path)
        reader = MultiProcessCameraReader(
            camera_id=CONFIG.reader_camera_id, fps=CONFIG.reader_scanning_fps
        )
        reader.start()
    except Exception as e:
        logger.error(f"early initialization failed: {e}")
        sys.exit(1)

    def exit_handler(sig, frame):
        reader.stop()
        sys.exit(0)

    # register signal handlers (for parent process to stop gracefully)
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    logger.info("gesture recognizer started")

    # main loop (suppress exceptions but log them)
    while True:
        try:
            with fps_controller(CONFIG.recognizer_scanning_fps):
                cv_img = reader.read()
                gst = recognizer.recognize(cv_img)

                state, gesture = filter.filter(gst)
                cmd = mapper.map(gesture, state)
                if cmd is not None:
                    logger.info(f"gesture: {gesture}, state: {state}, cmd: {cmd}")
                    queue.put(gesture)
        except Exception as e:
            logger.error(f"recognizer error: {e}")
