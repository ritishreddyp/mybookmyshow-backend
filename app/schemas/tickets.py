from pydantic import BaseModel 
from datetime import datetime


class tickets(BaseModel):
    ticket_id: int
    booking_id: int
    show_id: int
    ticket_code: str
    ticket_status: str
    issued_at: datetime
    updated_at: datetime
