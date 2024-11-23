from typer import Typer, Option
import uvicorn
from .. import app
from ..config import CONFIG

subcommand = Typer()


@subcommand.command(help="Run server")
def run(
    host: str = Option("127.0.0.1", help="Server host"),
    port: int = Option(8000, help="Server port"),
):
    uvicorn.run(app, host=host, port=port, log_level=CONFIG.log_level)
