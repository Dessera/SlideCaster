from fastapi import APIRouter, WebSocket
from ..models.control_model import Command, Gesture
from ..services.control_service import ControlService

router = APIRouter(tags=["control"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        value: Command = await ControlService().get()
        await websocket.send_text(value)


@router.post("/on")
async def on_gesture_event(gesture: Gesture):
    operation: Command = ControlService().parse(gesture)
    await ControlService().put(operation)
