from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class PaymentProcessRequest(BaseModel):
    booking_id : UUID
    payment_method : str


class PaymentDetails(BaseModel):
    payment_id : UUID
    booking_id : UUID
    transaction_id : str
    payment_method : str
    amount : float
    payment_status : str
    payment_date : datetime
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)