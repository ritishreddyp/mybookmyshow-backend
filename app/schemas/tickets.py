from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.payments import PaymentDetails
from uuid import UUID


class TicketOut(BaseModel):
    ticket_id : UUID
    booking_id : UUID
    show_id : UUID
    ticket_code : str
    ticket_status : str
    issued_at : datetime
    updated_at : datetime
    model_config = ConfigDict(from_attributes=True)


class BookingConfirmation(BaseModel):
    booking_id : UUID
    total_amount : float
    booking_status : str
    ticket : TicketOut
    payment : PaymentDetails
    model_config = ConfigDict(from_attributes=True)