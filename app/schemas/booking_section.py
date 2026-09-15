from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class BookingCreate(BaseModel):
    show_id : UUID
    show_seat_id : list[int]

class BookingStatusUpdate(BaseModel):
    booking_status: str

class BookingSectionResponse(BaseModel):
    booking_id: UUID
    show_id: UUID
    total_amount: float
    booking_status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)