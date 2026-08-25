from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.crud import create_language,assign_languages_to_movie,update_language,delete_language,get_languages_by_movie,get_movies_by_language,remove_language_from_movie
from app.schemas.languages import LanguageCreate,LanguageDetails,MovieLanguageAssignment,LanguageUpdate

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_language(language: LanguageCreate, db: Session = Depends(get_db)):
    return create_language(language, db)

@router.put("/{language_id}")
def edit_language(language_id: int, language: LanguageUpdate, db: Session = Depends(get_db)):
    return update_language(language_id, language, db)

@router.delete("/{language_id}")
def remove_language(language_id: int, db: Session = Depends(get_db)):
    return delete_language(language_id, db)

@router.post("/movies/{movie_id}/assign")
def assign_languages(movie_id: int, assignment: MovieLanguageAssignment, db: Session = Depends(get_db)):
    return assign_languages_to_movie(movie_id, assignment, db)

@router.delete("/movies/{movie_id}/remove/{language_id}")
def remove_language_movie(movie_id: int, language_id: int, db: Session = Depends(get_db)):
    return remove_language_from_movie(movie_id, language_id, db)


@router.get("/{language_id}/movies")
def view_movies_by_language(language_id: int, db: Session = Depends(get_db)):
    return get_movies_by_language(language_id, db)

@router.get("/movies/{movie_id}/languages")
def view_languages_by_movie(movie_id: int, db: Session = Depends(get_db)):
    return get_languages_by_movie(movie_id, db)