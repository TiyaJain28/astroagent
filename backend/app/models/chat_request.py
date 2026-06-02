from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    date: str
    time: str
    place: str