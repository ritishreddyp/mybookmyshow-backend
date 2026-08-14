from pydantic import BaseModel 
from datetime import datetime

class booking_section(BaseModel):
    booking_id: int
    user_id: int
    booking_type: str
    booking_date: datetime
    total_amount: float
    booking_status: str