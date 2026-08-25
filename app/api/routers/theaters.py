from fastapi import APIRouter, Depends,status,Query
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.models.theatres import SQtheaters
from app.schemas.theatres import TheatreCreate,TheatreDetails,TheatreUpdate
from app.crud import create_theater,get_all_theaters,get_theater_by_id,update_theater,delete_theater

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_theater(theater: TheatreCreate, db: Session = Depends(get_db)):
    return create_theater(theater, db)


@router.get("/")
def list_theaters(city_id: int | None = Query(None, description="Filter theaters by city ID"), db: Session = Depends(get_db)):
    return get_all_theaters(city_id, db)


@router.get("/{theater_id}", response_model=TheatreDetails)
def get_single_theater(theater_id: int, db: Session = Depends(get_db)):
    return get_theater_by_id(theater_id, db)


@router.put("/{theater_id}")
def edit_theater(theater_id: int, theater: TheatreUpdate, db: Session = Depends(get_db)):
    return update_theater(theater_id, theater, db)


@router.delete("/{theater_id}")
def remove_theater(theater_id: int, db: Session = Depends(get_db)):
    return delete_theater(theater_id, db)