from pydantic import BaseModel 
from datetime import datetime

class payments(BaseModel):
    payment_id: int
    booking_id: int
    transaction_id: str
    payment_method: str
    amount: float
    payment_status: str
    payment_date: datetime
    created_at: datetime