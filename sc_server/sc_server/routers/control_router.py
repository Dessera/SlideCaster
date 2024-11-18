from fastapi import APIRouter, WebSocket

router = APIRouter(tags=["control"], prefix="/control")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    pass


@router.post("/on/{command}")
async def on_gesture_command(command: str):
    pass
