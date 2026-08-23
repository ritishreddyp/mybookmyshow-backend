from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.crud import get_all_cities,get_city_id,create_city,delete_city
from app.schemas.city import  CityDetails,CityCreate

router = APIRouter()


@router.get("/")
def list_cities(db: Session = Depends(get_db)):
    return get_all_cities(db)


@router.get("/{city_id}")
def select_city(city_id: int, db: Session = Depends(get_db)):
    return get_city_id(city_id, db)


@router.post("/")
def add_city(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(city, db)

@router.delete("/")
def remove_city(city_id: int, db: Session = Depends(get_db)):
    return delete_city(city_id,db)

