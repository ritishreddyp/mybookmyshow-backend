from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List

class ShowSeatCreate(BaseModel):
    show_id: int
    seat_id: int
    price: float
    status: str = "available"
    
class SeatBookingRequest(BaseModel):
    show_id: int
    show_seat_ids: List[int]

class ShowSeatStatusUpdate(BaseModel):
    status : str 

class ShowSeatDetails(BaseModel):
    show_seat_id : int
    show_id : int
    seat_id : int
    price : float
    status : str  
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)