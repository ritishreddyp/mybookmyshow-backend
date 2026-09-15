from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.user import SQUser
from uuid import UUID

from app.api.deps import require_role
from app.core.db import get_db

from app.schemas.booking_section import BookingCreate
from app.curd_operations.booking import select_seats_and_create_summary, delete_booking_item

router = APIRouter()

@router.post("/")
def proceed_to_order_summary( booking_data: BookingCreate, db: Session = Depends(get_db), current_user: SQUser = Depends(require_role(["public", "user", "theater_admin", "admin"]))):
    user_identifier = getattr(current_user, "user_id", None) or getattr(current_user, "admin_id", None)
    return select_seats_and_create_summary(booking_data, user_identifier , db)

@router.delete("/{booking_id}/items/{booking_item_id}")
def remove_item_from_cart(booking_id: UUID, booking_item_id: UUID, db: Session = Depends(get_db), current_user: SQUser = Depends(require_role(["user", "theater_admin", "admin"]))):
    return delete_booking_item(booking_id, booking_item_id, current_user.user_id, db)