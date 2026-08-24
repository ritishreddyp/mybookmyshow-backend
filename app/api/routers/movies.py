from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.crud import create_movie,movie_update,delete_movie,get_all_movies,get_movie_id
from app.schemas.movies import  MovieCreate,MovieUpdate,MovieDetails

from app.crud import create_language,get_all_languages,get_movies_by_language_id,remove_language_from_movie
from app.schemas.languages import LanguageCreate,LanguageDetails

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

@router.delete("/")
def remove_movie(movie_id: int, db: Session = Depends(get_db)):
    return delete_movie(movie_id,db)

@router.get("/")
def movies_list(db: Session = Depends(get_db)):
    return get_all_movies(db)


@router.get("/{movie_id}")
def select_movie(movie_id: int, db: Session = Depends(get_db)):
    return get_movie_id(movie_id, db)



@router.post("/language")
def add_new_language(lang_in: LanguageCreate, db: Session = Depends(get_db)):
    return create_language(lang_in, db)

@router.get("/language" )
def list_languages(db: Session = Depends(get_db)):
    return get_all_languages(db)

@router.get("/{language_id}/movies")
def get_movies_by_language(language_id: int, db: Session = Depends(get_db)):
    return get_movies_by_language_id(language_id, db)

@router.delete("/language")
def remove_movie_from_language(language_id:int,db:Session= Depends(get_db)):
    return remove_language_from_movie(language_id,db)