from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session

from app.core.db import get_db
from uuid import UUID

from app.schemas.show_seats import ShowSeatDetails
from app.curd_operations.show_seat import get_show_seats,generate_show_seats_for_show,update_show_seat,delete_show_seat, restore_show_seat


router = APIRouter()

#public access
@router.get("/show/{show_id}")
def view_show_seats(show_id: UUID, db: Session = Depends(get_db)):
    return get_show_seats(show_id, db)

# admin access
@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_seats_for_show(show_id: UUID, screen_id: UUID, base_price: float, db: Session = Depends(get_db)):
    generate_show_seats_for_show(show_id, screen_id, base_price, db)
    return {"message": "Show seats generated successfully"}

@router.patch("/{show_seat_id}")
def modify_show_seat(show_seat_id: int, status: str | None = None, price: float | None = None, db: Session = Depends(get_db)):
    return update_show_seat(show_seat_id, status, price, db)

@router.delete("/show/{show_id}/seat/{show_seat_id}")
def remove_show_seat(show_id: UUID, show_seat_id: int, db: Session = Depends(get_db)):
    return delete_show_seat(show_id, show_seat_id, db)

# Restore a soft-deleted show seat
@router.post("/show/{show_id}/seat/{show_seat_id}/restore")
def restore_seat_endpoint(show_id: UUID, show_seat_id: int, db: Session = Depends(get_db)):
    return restore_show_seat(show_id, show_seat_id, db)