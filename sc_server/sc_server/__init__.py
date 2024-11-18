from fastapi import FastAPI
from .routers import include_app_routers
from .error import include_app_error_handlers


def create_app() -> FastAPI:
    """创建FastAPI实例，挂载路由、中间件、错误处理等

    Returns:
        FastAPI: FastAPI实例
    """
    app = FastAPI(title="SC Server")

    include_app_routers(app)
    include_app_error_handlers(app)

    return app


app = create_app()
