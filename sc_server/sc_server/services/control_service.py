import multiprocessing as mp

from ..config import CONFIG
from ..submodule.recognizer import entry as recognizer_entry

_queue = mp.Queue(maxsize=CONFIG.command_queue_size)
_proc = mp.Process(target=recognizer_entry, args=(_queue,))


def get_command():
    return _queue.get()


def start_client():
    global _proc
    if _proc.is_alive():
        return False
    _proc = mp.Process(target=recognizer_entry, args=(_queue,))
    _proc.start()
    return True


def client_status():
    return _proc.is_alive()


def stop_client():
    if not _proc.is_alive():
        return False
    _proc.terminate()
    _proc.join()
    return True


def restart_client():
    stop_client()
    return start_client()


def upload_model(file: bytes):
    with open(CONFIG.model_path, "wb") as f:
        f.write(file)


def upload_map(file: bytes):
    with open(CONFIG.map_path, "wb") as f:
        f.write(file)
