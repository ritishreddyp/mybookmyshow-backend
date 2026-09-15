from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.api.deps import require_role

from app.schemas.tickets import BookingConfirmation

from app.curd_operations.ticket import get_ticket_details

router = APIRouter()


@router.get("/{booking_id}")
def get_m_ticket(booking_id: int, db: Session = Depends(require_role(["admin","user"]))):
    current_user_id = 1
    return get_ticket_details(booking_id, current_user_id, db)