from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.city import SQcity
from app.schemas.city import CityCreate,CityDetails


#---------------------------------------------------------- city operations ---------------------------------------------------------#

# to get city details
def get_all_cities(db: Session):
    return db.query(SQcity).filter(SQcity.is_active == True).all()


# to get one city 
def get_city_id(city_id: int, db: Session):
    cities = db.query(SQcity).filter(SQcity.city_id == city_id).first()
    if cities is None:
            raise HTTPException(status_code=404, detail="City not found")
    
    return cities


# to add city 
def create_city(city: CityCreate, db: Session):
    existing_city =db.query(SQcity).filter((SQcity.city_name == city.city_name)).first()
    if existing_city:
        raise HTTPException(status_code=400,detail="city already exists")
    new_city = SQcity(city_name=city.city_name,state=city.state)

    db.add(new_city)
    db.commit()

    return " city added successfully"

  
# to delete city 
def delete_city(city_id: int, db: Session):
    city = db.query(SQcity).filter(SQcity.city_id == city_id).first()
    if not city:
            raise HTTPException(status_code=404, detail="City not found")

    city.is_active = False
    db.commit()

    return " city deleted succesfully "


# to get inactive city
def get_inactive_cities(db: Session):
    return db.query(SQcity).filter(SQcity.is_active == False).all()


# to update inactive city
def restore_city(city_id: int, db: Session):
    city = db.query(SQcity).filter(SQcity.city_id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    city.is_active = True
    db.commit()
    db.refresh(city)
    return "City activated successfully"