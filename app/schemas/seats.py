from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SeatCreate(BaseModel):
    screen_id : int
    seat_number : str  
    seat_row : str    
    seat_type : str 


class SeatDetails(BaseModel):
    seat_id : int
    screen_id : int
    seat_number : str
    seat_row : str
    seat_type : str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)