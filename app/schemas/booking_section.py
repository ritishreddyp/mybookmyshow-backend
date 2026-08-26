from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    show_id : int
    seat_ids : list[int]

class BookingStatusUpdate(BaseModel):
    booking_status: str

class BookingSectionResponse(BaseModel):
    booking_id: int
    show_id: int
    total_amount: float
    booking_status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)