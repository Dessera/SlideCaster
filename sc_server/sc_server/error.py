from fastapi import FastAPI
from fastapi.responses import JSONResponse


def include_app_error_handlers(app: FastAPI):
    """注册应用程序错误处理程序

    Args:
        app (FastAPI): FastAPI 实例
    """
    # unknown error handler
    app.add_exception_handler(Exception, __handle_unknown_error)


def __handle_unknown_error(_, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "未知错误", "detail": str(exc)},
    )
