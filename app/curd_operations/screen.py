from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID

from app.models.screens import SQscreens
from app.schemas.screens import ScreenCreate,ScreenUpdate,ScreenDetails

from app.models.theaters import SQtheaters

#-------------------------------------------------------screens---------------------------------------------------

#to add screens to theater 
def add_screen_to_theater(theater_id: UUID, screen_name: str, screen_type: str, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")

    new_screen = SQscreens(
        theater_id=theater_id,
        screen_name=screen_name,
        screen_type=screen_type,
        status="active" )
    
    try:

        db.add(new_screen)
        db.commit()
        db.refresh(new_screen)

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to add screen: {e}")

    return "Screen added successfully"


# Update Screens
def update_screen(screen_id: UUID, screen_update: ScreenUpdate, db: Session):
    screen = db.query(SQscreens).filter(SQscreens.screen_id == screen_id).first()
    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found")

    update_data = screen_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(screen, key, value)

    try:
        db.commit()
        db.refresh(screen)

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update screen: {e}")

    return "Screen updated successfully"


# Delete Screen
def delete_screen(screen_id: UUID, db: Session):
    screen = db.query(SQscreens).filter(SQscreens.screen_id == screen_id).first()
    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found")
    
    try:
        screen.is_active = False
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete screen: {e}")

    return "Screen deleted successfully"


# to get active screens in theater
def get_screens_by_theater(theater_id: UUID, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")
    
    return [screen for screen in theater.screens if screen.is_active]


#to get inactive screens
def get_inactive_screens_by_theater(theater_id: UUID, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")
    
    return [screen for screen in theater.screens if not screen.is_active]


# to activate screens
def activate_screen(screen_id: UUID, db: Session):
    screen = db.query(SQscreens).filter(SQscreens.screen_id == screen_id).first()
    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found")
    
    try:
        screen.is_active = True
        db.commit()
        db.refresh(screen)

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to activate screen: {e}")

    return "Screen activated successfully"
