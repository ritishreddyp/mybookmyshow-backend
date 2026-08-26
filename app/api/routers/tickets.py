from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.schemas.tickets import BookingConfirmation

from app.crud import get_ticket_details

router = APIRouter()


@router.get("/{booking_id}", response_model=BookingConfirmation, status_code=status.HTTP_200_OK)
def get_m_ticket(booking_id: int, db: Session = Depends(get_db)):
    current_user_id = 1
    return get_ticket_details(booking_id=booking_id, user_id=current_user_id, db=db)