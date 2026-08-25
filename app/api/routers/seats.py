from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.seats import SeatCreate
from app.crud import generate_seats_for_screen,delete_seats_for_screen,update_seats_for_screen

router = APIRouter()

@router.post("/seat-generate", status_code=status.HTTP_201_CREATED)
def generate_seats(hall : SeatCreate, db: Session = Depends(get_db)):
    return generate_seats_for_screen(hall, db)

@router.delete("/theater/{theater_id}/screen/{screen_id}/seats")
def remove_screen_seats(theater_id: int, screen_id: int, db: Session = Depends(get_db)):
    return delete_seats_for_screen(theater_id, screen_id, db)

@router.patch("/theater/{theater_id}/screen/{screen_id}/seats-type")
def modify_screen_seats_type(theater_id: int, screen_id: int, new_seat_type: str, db: Session = Depends(get_db)):
    return update_seats_for_screen(theater_id, screen_id, new_seat_type, db)