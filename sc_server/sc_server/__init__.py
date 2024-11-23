from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import include_app_routers
from .services import control_service
from .error import include_app_error_handlers


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    yield
    # cleanup sub-processes
    control_service.stop_client()


def create_app() -> FastAPI:
    app = FastAPI(title="SC Server", lifespan=app_lifespan)

    include_app_routers(app)
    include_app_error_handlers(app)

    return app


app = create_app()
