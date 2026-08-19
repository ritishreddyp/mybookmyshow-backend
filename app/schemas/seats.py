from pydantic import BaseModel 
from datetime import datetime


class seats(BaseModel):
    seat_id: int
    screen_id: int
    seat_number: str
    seat_row: str
    seat_type: str
    created_at: datetime
    updated_at: datetime