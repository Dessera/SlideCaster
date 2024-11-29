from fastapi import APIRouter, UploadFile, WebSocket, WebSocketDisconnect

from ..services.control_service import ControlService
from ..config import CONFIG

router = APIRouter(tags=["control"], prefix="/control")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ControlService().manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ControlService().manager.disconnect(websocket)


@router.get("/status")
def get_client_status():
    return ControlService().client_status()


@router.post("/start")
def start_client():
    return ControlService().start_client()


@router.post("/stop")
def stop_client():
    return ControlService().stop_client(CONFIG.subprocess_timeout)


@router.post("/model")
async def upload_model(file: UploadFile):
    return ControlService().upload_model(await file.read())


@router.post("/map")
async def upload_map(file: UploadFile):
    return ControlService().upload_map(await file.read())
