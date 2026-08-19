from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ShowSeatCreate(BaseModel):
    show_id : int
    seat_id : int
    price : float
    status : str = "available"


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