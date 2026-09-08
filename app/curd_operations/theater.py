from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.theatres import SQtheaters
from app.schemas.theatres import TheatreCreate,TheatreUpdate,TheatreDetails

from app.models.city import SQcity
# -----------------------------------------------------------theaters-------------------------------------------------------------- 

# to create theaters 
def create_theater(theater: TheatreCreate, db: Session):
    city = db.query(SQcity).filter(SQcity.city_id == theater.city_id).first()
    if not city:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="City not found")

    new_theater = SQtheaters(**theater.model_dump())

    try:
        db.add(new_theater)
        db.commit()
        db.refresh(new_theater)

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create theater: {e}")

    return "Theater added successfully"


# to update theaters
def update_theater(theater_id: int, theater_update: TheatreUpdate, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")

    update_data = theater_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(theater, key, value)

    try:
        db.commit()
        db.refresh(theater)

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update theater: {e}")

    return "Theater updated successfully"


#remvoe theaters
def delete_theater(theater_id: int, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")

    try:
        theater.is_active = False
        db.delete(theater)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete theater: {e}")
    
    return "Theater deleted successfully"


#to get all active theaters
def get_all_theaters(city_id: int | None, db: Session):
    query = db.query(SQtheaters).filter(SQtheaters.is_active == True)
    if city_id:
        query = query.filter(SQtheaters.city_id == city_id)
    return query.all()


# to get inactive theaters
def get_inactive_theaters(db: Session):
    return db.query(SQtheaters).filter(SQtheaters.is_active == False).all()


# to get theater by id
def get_theater_by_id(theater_id: int, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")
    return theater
