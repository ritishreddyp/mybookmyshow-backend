from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.booking_section import BookingCreate
from app.crud import select_seats_and_create_summary, delete_booking_item

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def proceed_to_order_summary(booking_data: BookingCreate, db: Session = Depends(get_db)):
    current_user_id = 1 
    return select_seats_and_create_summary(booking_data, current_user_id, db)


@router.delete("/{booking_id}/items/{booking_item_id}", status_code=status.HTTP_200_OK)
def remove_item_from_cart(booking_id: int, booking_item_id: int, db: Session = Depends(get_db)):
     current_user_id = 1  
     return delete_booking_item(booking_id, booking_item_id, current_user_id, db)