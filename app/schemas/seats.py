from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SeatCreate(BaseModel):
    theater_id: UUID
    screen_id : UUID
    rows : list[str] 
    seats_per_row : int   
    seat_type : str 


class SeatDetails(BaseModel):
    id : UUID
    screen_id : UUID
    rows : str
    seats_per_row : str
    seat_type : str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)