from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.payments import PaymentDetails


class TicketOut(BaseModel):
    ticket_id : int
    booking_id : int
    show_id : int
    ticket_code : str
    ticket_status : str
    issued_at : datetime
    updated_at : datetime
    model_config = ConfigDict(from_attributes=True)


class BookingConfirmation(BaseModel):
    booking_id : int
    total_amount : float
    booking_status : str
    ticket : TicketOut
    payment : PaymentDetails
    model_config = ConfigDict(from_attributes=True)