import time
import asyncio
from contextlib import contextmanager, asynccontextmanager


@contextmanager
def fps_controller(fps: float):
    start_time = time.time()
    yield
    end_time = time.time()
    time_cost = end_time - start_time
    time_left = 1 / fps - time_cost
    if time_left > 0:
        time.sleep(time_left)


@asynccontextmanager
async def async_fps_controller(fps: float):
    start_time = time.time()
    yield
    end_time = time.time()
    time_cost = end_time - start_time
    time_left = 1 / fps - time_cost
    if time_left > 0:
        await asyncio.sleep(time_left)
