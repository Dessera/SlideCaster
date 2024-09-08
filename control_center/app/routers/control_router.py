from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from asyncio import Queue

router = APIRouter(tags=["control"])

buffer: Queue[str] = Queue(maxsize=5)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            value = await buffer.get()
            await websocket.send_text(value)
        except WebSocketDisconnect:
            break
        except Exception as e:
            print(f"Websocket error: {e}")
            break


@router.post("/on/{event_name}/{event_type}")
async def on_gesture_event(event_name: str, event_type: str):
    gesture_to_operation = {
        "Thumb_Up": {
            "short": "page_up",
            "long": "page_up",
        }
    }
    mapped_gesture = gesture_to_operation.get(event_name)
    if not mapped_gesture:
        return
    operation = mapped_gesture.get(event_type)
    if not operation:
        return
    await buffer.put(operation)
