from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import include_app_routers
from .services import control_service
from .error import include_app_error_handlers
from .config import CONFIG


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    yield
    # cleanup sub-processes
    control_service.stop_client()


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

    return app


app = create_app()
