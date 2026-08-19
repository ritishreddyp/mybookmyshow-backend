from pydantic import BaseModel 
from datetime import datetime

class theatres(BaseModel):
    theater_id: int
    city_id: int
    theater_name: str
    address: str
    contact_number: str
    status: str
    created_at: datetime
    updated_at: datetime