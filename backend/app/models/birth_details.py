from pydantic import BaseModel


class BirthDetails(BaseModel):
    date: str
    time: str
    place: str