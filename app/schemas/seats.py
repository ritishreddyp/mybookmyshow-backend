from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SeatCreate(BaseModel):
    theater_id: int
    screen_id : int
    rows : list[str] 
    seats_per_row : int   
    seat_type : str 


class SeatDetails(BaseModel):
    id : int
    screen_id : int
    rows : str
    seats_per_row : str
    seat_type : str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)