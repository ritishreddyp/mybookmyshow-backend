from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PaymentProcessRequest(BaseModel):
    booking_id : int
    payment_method : str


class PaymentDetails(BaseModel):
    payment_id : int
    booking_id : int
    transaction_id : str
    payment_method : str
    amount : float
    payment_status : str
    payment_date : datetime
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)