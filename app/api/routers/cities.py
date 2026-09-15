from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.api.deps import require_role

from app.curd_operations.city import get_all_cities,get_city_id,create_city,delete_city,restore_city,get_inactive_cities
from app.schemas.city import  CityDetails,CityCreate

router = APIRouter()

# public access 
@router.get("/")
def list_cities(db: Session = Depends(get_db)):
    return get_all_cities(db)

# admin access
@router.get("/inactive")
def list_inactive_cities(db: Session = Depends(get_db), current_user = Depends(require_role(["admin"]))):
    return get_inactive_cities(db)

# public access 
@router.get("/{city_id}")
def select_city(city_id: UUID , db: Session = Depends(get_db)):
    return get_city_id(city_id, db)


# admin access
@router.post("/")
def add_city(city: CityCreate, db: Session =Depends(get_db),current_user = Depends(require_role(["admin"]))):
    return create_city(city, db)

@router.delete("/{city_id}")
def remove_city(city_id: UUID, db: Session =Depends(get_db),current_user = Depends(require_role(["admin"]))):
    return delete_city(city_id,db)

@router.patch("/{city_id}/activate")
def activate_city(city_id: UUID, db: Session =Depends(get_db),current_user = Depends(require_role(["admin"]))):
    return restore_city(city_id, db)


