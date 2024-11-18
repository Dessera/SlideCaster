from fastapi import APIRouter, WebSocket

from ..services import control_service

router = APIRouter(tags=["control"], prefix="/control")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        cmd = await control_service.get_command()
        await websocket.send_text(cmd)


@router.post("/on/{command}")
async def on_gesture_command(command: str):
    await control_service.put_command(command)
