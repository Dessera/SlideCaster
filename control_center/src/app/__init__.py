from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .routers import control_router
from .models.control_model import GestureParsedError


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(control_router.router, prefix="/control")

    app.add_exception_handler(GestureParsedError, handle_gesture_error)

    return app


def handle_gesture_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
