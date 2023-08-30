from pydantic import BaseModel, EmailStr

class DatetimeModel(BaseModel):
    dateTime : str
    timeZone: str

class ReserveModel(BaseModel):
    summary: str
    location: str | None = None #look how to reserve a room (like location)
    start: DatetimeModel
    end: DatetimeModel
    attendees: list[dict[str,EmailStr]] | None = None
    reminders: dict | None = None

class ReserveBotResponse(BaseModel):
    id: str
    status: str
    summary: str

class DeleteEvent(BaseModel):
    id: str

