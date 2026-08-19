from pydantic import BaseModel 
from datetime import datetime

class bookings(BaseModel):
    booking_id: int
    user_id: int
    show_id: int
    total_amount: float
    booking_status: str
    created_at: datetime
    updated_at: datetime