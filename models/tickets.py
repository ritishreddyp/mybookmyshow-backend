from pydantic import BaseModel 
from datetime import datetime

class tickets(BaseModel):
    ticket_id	: int
    booking_id	: int
    ticket_code :str
    qr_code	:str 
    issued_at	:datetime
    ticket_status	:str