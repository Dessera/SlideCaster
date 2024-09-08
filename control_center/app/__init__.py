from fastapi import FastAPI
from .routers import control_router


def create_app():
    app = FastAPI()

    app.include_router(control_router.router, prefix="/control")

    return app


app = create_app()
