import os
import shutil
from typer import Typer, Option
import uvicorn
from .. import app
from ..config import CONFIG

subcommand = Typer()


def get_project_root():
    current_path = os.path.dirname(__file__)  # sc_server/cli
    return os.path.dirname(current_path)  # sc_server


def get_default_model():
    return os.path.join(get_project_root(), "submodule/recognizer/default/model.task")


def get_default_map():
    return os.path.join(get_project_root(), "submodule/recognizer/default/map.json")


@subcommand.command(help="Run server")
def run(
    host: str = Option("127.0.0.1", help="Server host"),
    port: int = Option(8000, help="Server port"),
):
    uvicorn.run(app, host=host, port=port, log_level=CONFIG.log_level.lower())


@subcommand.command(help="Init default files & dirs for server")
def init(
    default_model: str = Option(get_default_model(), help="Path to default model"),
    default_map: str = Option(get_default_map(), help="Path to default map"),
):
    try:
        # input validation
        if not os.path.exists(default_model):
            raise FileNotFoundError(f"Default model not found: {default_model}")
        if not os.path.exists(default_map):
            raise FileNotFoundError(f"Default map not found: {default_map}")

        # create dirs
        target_base_path = os.path.dirname(CONFIG.file_base)
        target_model_path = os.path.dirname(CONFIG.model_path)
        target_map_path = os.path.dirname(CONFIG.map_path)

        if not os.path.exists(target_base_path):
            os.makedirs(target_base_path)
            print(f"Creating base path: {target_base_path}")
        if not os.path.exists(target_model_path):
            os.makedirs(target_model_path)
            print(f"Creating model path: {target_model_path}")
        if not os.path.exists(target_map_path):
            os.makedirs(target_map_path)
            print(f"Creating map path: {target_map_path}")

        # copy default files
        shutil.copy(default_model, CONFIG.model_path)
        print(f"Copying default model to {CONFIG.model_path}")

        shutil.copy(default_map, CONFIG.map_path)
        print(f"Copying default map to {CONFIG.map_path}")

    except Exception as e:
        print(f"server init failed: {e}")
