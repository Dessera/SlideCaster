from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import include_app_routers
from .services.control_service import ControlService
from .error import include_app_error_handlers
from .config import CONFIG


def get_package_root():
    return os.path.dirname(__file__)


def get_static_path():
    return os.path.join(get_package_root(), "submodule/reader")


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    ControlService().start()
    yield
    # cleanup sub-processes
    ControlService().stop()


def create_app() -> FastAPI:
    app = FastAPI(title="SC Server", lifespan=app_lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[CONFIG.app_base_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_app_routers(app)
    include_app_error_handlers(app)

    # app.mount("/", StaticFiles(directory=get_static_path(), html=True), name="reader")

    return app


app = create_app()
