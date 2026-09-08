from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.tickets import SQtickets
from app.schemas.tickets import TicketOut,BookingConfirmation

from app.models.payments import SQpayments
from app.curd_operations.payment import get_user_booking
# -------------------------------------------------------tickets -------------------------------------------------

# to genrate tickets
def get_ticket_details(booking_id: int, user_id: int, db: Session):

    booking = get_user_booking(booking_id, user_id, db)
    ticket = db.query(SQtickets).filter_by(booking_id=booking_id).first()
    payment = db.query(SQpayments).filter_by(booking_id=booking_id).first()

    if not ticket:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="M-Ticket not found for this booking.")
    
    return {"booking_id": booking.booking_id, "total_amount": booking.total_amount, "booking_status": booking.booking_status, "ticket": ticket, "payment": payment}