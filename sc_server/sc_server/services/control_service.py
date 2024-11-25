import asyncio
import multiprocessing as mp

from ..utils.connection_manager import ConnectionManager
from ..utils.singleton import singleton
from ..utils.async_proc_queue import AsyncProcQueue

from ..config import CONFIG
from ..submodule.recognizer import entry as recognizer_entry


@singleton
class ControlService:
    m_queue = AsyncProcQueue(maxsize=CONFIG.command_queue_size)
    manager = ConnectionManager()

    m_proc: mp.Process | None = None
    m_task: asyncio.Task | None = None

    async def get_command(self):
        return await self.m_queue.coro_get()

    def start_background_task(self):
        async def background_task():
            while True:
                command = await self.get_command()
                await self.manager.broadcast(command)

        self.m_task = asyncio.create_task(background_task())

    def stop_background_task(self):
        if self.m_task is not None:
            self.m_task.cancel()

    def start_client(self):
        if self.m_proc is not None and self.m_proc.is_alive():
            return False
        self.m_proc = mp.Process(target=recognizer_entry, args=(self.m_queue,))
        self.m_proc.start()
        return True

    def client_status(self):
        return self.m_proc.is_alive() if self.m_proc is not None else False

    def stop_client(self, timeout: float | None = None):
        if self.m_proc is not None and self.m_proc.is_alive():
            self.m_proc.terminate()
            self.m_proc.join(timeout)
            return True
        return False

    def upload_model(self, file: bytes):
        with open(CONFIG.model_path, "wb") as f:
            f.write(file)

    def upload_map(self, file: bytes):
        with open(CONFIG.map_path, "wb") as f:
            f.write(file)

    def start(self):
        self.start_background_task()
        self.start_client()

    def stop(self):
        self.stop_client(CONFIG.subprocess_timeout)
        self.stop_background_task()
