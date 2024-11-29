from typer import Typer
from . import server_cli

app = Typer()

app.add_typer(server_cli.subcommand, name="server")
