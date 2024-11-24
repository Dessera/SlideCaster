from fastapi import APIRouter, UploadFile, WebSocket

from ..services import control_service

router = APIRouter(tags=["control"], prefix="/control")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        cmd = await control_service.get_command()
        await websocket.send_text(cmd)


@router.get("/status")
def get_client_status():
    return control_service.client_status()


@router.post("/start")
def start_client():
    return control_service.start_client()


@router.post("/stop")
def stop_client():
    return control_service.stop_client()


@router.post("/model")
async def upload_model(file: UploadFile):
    return control_service.upload_model(await file.read())


@router.post("/map")
async def upload_map(file: UploadFile):
    return control_service.upload_map(await file.read())
