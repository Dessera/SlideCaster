from typing import Literal
from pydantic import BaseModel


type GestureLabel = Literal["Thumb_Up", "Thumb_Down", "Open_Palm", "Closed_Fist"]
type GestureOperation = Literal["short", "long"]


class Gesture(BaseModel):
    label: GestureLabel
    operation: GestureOperation


type Command = Literal["page:next", "page:prev", "scale:up", "scale:down"]


class GestureParsedError(Exception):
    def __init__(self, gesture: Gesture):
        self.gesture = gesture
        self.message = f"Gesture {gesture.label} {gesture.operation} cannot be parsed"
        super().__init__(self.message)
