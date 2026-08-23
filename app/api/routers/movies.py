from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.crud import create_movie,movie_update
from app.schemas.movies import  MovieCreate,MovieUpdate,MovieDetails
router = APIRouter()

@router.post("/")
def add_movie( movie : MovieCreate,db: Session = Depends(get_db)):
    return create_movie(movie,db)

@router.patch("/{movie_id}")
def update_movie_details(movie_id:int, movie: MovieUpdate,db: Session = Depends(get_db)):
    return movie_update(movie_id,movie,db)

@router.patch("/{movie_id}", response_model=MovieDetails)
def update_movie_details(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    return movie_update(movie_id, movie, db)