import asyncio
import multiprocessing as mp

from concurrent.futures import ThreadPoolExecutor


class AsyncProcQueue:
    m_executor = ThreadPoolExecutor()

    m_queue: mp.Queue

    def __init__(self, maxsize: int = 0):
        self.m_queue = mp.Queue(maxsize=maxsize)

    async def coro_put(self, item):
        return await asyncio.get_event_loop().run_in_executor(
            self.m_executor, self.m_queue.put, item
        )

    async def coro_get(self):
        return await asyncio.get_event_loop().run_in_executor(
            self.m_executor, self.m_queue.get
        )

    @property
    def qsize(self):
        return self.m_queue.qsize

    @property
    def empty(self):
        return self.m_queue.empty

    @property
    def full(self):
        return self.m_queue.full

    @property
    def put(self):
        return self.m_queue.put

    @property
    def put_nowait(self):
        return self.m_queue.put_nowait

    @property
    def get(self):
        return self.m_queue.get

    @property
    def get_nowait(self):
        return self.m_queue.get_nowait
