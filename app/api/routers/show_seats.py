from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.schemas.show_seats import ShowSeatDetails
from app.curd_operations.show_seat import get_show_seats

router = APIRouter()

@router.get("/show/{show_id}")
def view_show_seats(show_id: int, db: Session = Depends(get_db)):
    return get_show_seats(show_id, db)

 