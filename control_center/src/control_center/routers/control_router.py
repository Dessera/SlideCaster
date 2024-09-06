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
            print("Websocket disconnected, wait for next connection")
        except Exception as e:
            print(f"Websocket error: {e}")


@router.post("/on/{event_name}")
async def on_gesture_event(event_name: str):
    gesture_map = {"Thumb_Up": "page_up"}
    mapped_event: str | None = gesture_map.get(event_name)
    if not mapped_event:
        print(f"Event {event_name} was ignored")
    else:
        await buffer.put(mapped_event)
