from pydantic import BaseModel 
from datetime import datetime

class show_seats(BaseModel):
    show_seat_id: int
    show_id: int
    seat_id: int
    price: float
    status: str
    created_at: datetime
    updated_at: datetime