import asyncio

from asyncio import Queue

from ..config import CONFIG

__queue: Queue[str] = Queue(maxsize=CONFIG.command_queue_size)


async def get_command() -> str:
    return await __queue.get()


async def put_command(command: str):
    await asyncio.wait_for(__queue.put(command), timeout=CONFIG.command_queue_timeout)


def start_client():
    pass


def client_status():
    pass


def stop_client():
    pass
