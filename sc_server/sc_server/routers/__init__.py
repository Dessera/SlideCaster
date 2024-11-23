from fastapi import FastAPI
from . import control_router, file_router


def include_app_routers(app: FastAPI):
    """挂载路由

    Args:
        app (FastAPI): FastAPI实例
    """
    app.include_router(control_router.router)
    app.include_router(file_router.router)
