from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.api.deps import require_role

from app.schemas.seats import SeatCreate
from app.curd_operations.seats import generate_seats_for_screen,delete_seats_for_screen,update_seats_for_screen

router = APIRouter()

#public access

@router.post("/seat-generate")
def generate_seats(hall : SeatCreate, db: Session = Depends(require_role(["theater_admin", "admin"]))):
    return generate_seats_for_screen(hall, db)

@router.delete("/theater/{theater_id}/screen/{screen_id}/seats")
def remove_screen_seats(theater_id: int, screen_id: int, db: Session = Depends(require_role(["theater_admin", "admin"]))):
    return delete_seats_for_screen(theater_id, screen_id, db)

@router.patch("/theater/{theater_id}/screen/{screen_id}/seats-type")
def modify_screen_seats_type(theater_id: int, screen_id: int, new_seat_type: str, db: Session = Depends(require_role(["theater_admin", "admin"]))):
    return update_seats_for_screen(theater_id, screen_id, new_seat_type, db)