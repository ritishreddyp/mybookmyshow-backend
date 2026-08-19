from pydantic import BaseModel 
from datetime import datetime


class booking_items(BaseModel):
    booking_item_id: int
    booking_id: int
    show_seat_id: int
    price: float
    created_at: datetime
    updated_at: datetime
    