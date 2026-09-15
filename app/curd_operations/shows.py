from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List
import uuid
from pathlib import Path

from app.models.shows import SQshows
from app.schemas.shows import ShowCreate, ShowUpdate

from app.models.screens import SQscreens
from app.models.movies import SQmovies
from app.models.languages import SQlanguages
from app.models.theaters import SQtheaters
from app.curd_operations.show_seat import generate_show_seats_for_show

#----------------------------------------------------shows---------------------------------------------------------------

# to create a show
def create_show(show: ShowCreate, db: Session):

    screen = db.query(SQscreens).filter(SQscreens.theater_id == show.theater_id, SQscreens.screen_id == show.screen_id).first()
    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found in this theater")

    movie = db.query(SQmovies).filter(SQmovies.movie_id == show.movie_id).first()
    if not movie:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Movie not found")

    language = db.query(SQlanguages).filter(SQlanguages.language_id == show.language_id).first()
    if not language:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Language not found")

    #time caluculation btwn shows
    new_start_time = datetime.combine(show.show_date, show.show_time).replace(tzinfo=None)
    buffer_minutes = 20 
    new_end_time = new_start_time + timedelta(minutes=movie.duration_minutes + buffer_minutes)

    existing_shows = db.query(SQshows).filter(SQshows.screen_id == screen.screen_id).all()
    for existing in existing_shows:
        existing_movie = db.query(SQmovies).filter(SQmovies.movie_id == existing.movie_id).first()

        if not existing_movie:
            continue

        existing_start_time = existing_start_time = datetime.combine(existing.show_date, existing.show_time).replace(tzinfo=None)
        existing_end_time = existing_start_time + timedelta(minutes=existing_movie.duration_minutes + buffer_minutes)
        if (existing_start_time < new_end_time) and (existing_end_time > new_start_time):
            raise HTTPException( status.HTTP_400_BAD_REQUEST, detail=f"Screen conflict: Slot occupied  ({existing_start_time.time()} - {existing_end_time.time()})." )

    new_show = SQshows(
        movie_id=show.movie_id,
        screen_id=screen.screen_id,
        language_id=show.language_id,
        show_date=show.show_date,
        show_time=show.show_time,
        base_price=show.base_price,
        status="active" )

    try:
        db.add(new_show)
        db.commit()
        db.refresh(new_show)

        generate_show_seats_for_show(show_id=new_show.show_id, screen_id=screen.screen_id,  base_price=show.base_price, db=db)

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create show: {e}")

    return "Show scheduled successfully"

# to update show details

def update_show(show_id: int, show_update: ShowUpdate, db: Session):
    show = db.query(SQshows).filter(SQshows.show_id == show_id).first()
    if not show:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Show not found")

    update_data = show_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(show, key, value)

    try:
        db.commit()
        db.refresh(show)

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update show: {e}")

    return "Show updated successfully"

# delete show

def delete_show(show_id: int, db: Session):
    show = db.query(SQshows).filter(SQshows.show_id == show_id).first()

    if not show:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Show not found")

    try:
        db.delete(show)
        db.commit()
    except Exception as e:
        db.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete show: {e}")

    return "Show deleted successfully"


# To view all shows 
def get_shows(
    city_id: int | None = None, 
    theater_id: int | None = None, 
    local_screen_id: int | None = None, 
    movie_id: int | None = None, 
    language_id: int | None = None, 
    db: Session = None):

    query = db.query(SQshows).join(SQscreens, SQshows.screen_id == SQscreens.screen_id).join(SQtheaters, SQscreens.theater_id == SQtheaters.theater_id)
    if city_id:
        query = query.filter(SQtheaters.city_id == city_id)
    if theater_id:
        query = query.filter(SQtheaters.theater_id == theater_id)
    if local_screen_id:
        query = query.filter(SQscreens.screen_id == local_screen_id)
    if movie_id:
        query = query.filter(SQshows.movie_id == movie_id)
    if language_id:
        query = query.filter(SQshows.language_id == language_id)

    return query.all()
