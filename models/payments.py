from pydantic import BaseModel 
from datetime import datetime

class payments(BaseModel):
    payment_id: int
    booking_id: int
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str
    payment_time: datetime