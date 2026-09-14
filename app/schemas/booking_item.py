from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class BookingItemAdd(BaseModel):
    show_seat_id: int

class BookingItemResponse(BaseModel):
    booking_item_id: UUID
    booking_id: UUID
    show_seat_id: int
    price: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)