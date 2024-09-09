from . import create_app
import uvicorn

app = create_app()
uvicorn.run(app)
