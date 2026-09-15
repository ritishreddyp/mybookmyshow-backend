from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.api.deps import require_role

from app.models.movies import SQmovies
from app.curd_operations.movie import create_movie,movie_update,delete_movie,get_movie_id,get_active_movies,get_inactive_movies,activate_movie
from app.schemas.movies import  MovieCreate,MovieUpdate,MovieDetails

from app.curd_operations.language import create_language,assign_languages_to_movie,update_language,delete_language,get_languages_by_movie,get_movies_by_language,remove_language_from_movie, get_inactive_languages, activate_language
from app.schemas.languages import LanguageCreate,MovieLanguageAssignment,LanguageUpdate

router = APIRouter()

# public access
@router.get("/")
def movies_list(db: Session = Depends(get_db)):
    return get_active_movies(db)

# admin access
@router.get("/inactive")
def list_inactive_movies(db: Session =Depends(get_db),  current_user = Depends(require_role(["theater_admin", "admin"]))):
    return get_inactive_movies(db)

#public 
@router.get("/{movie_id}")
def select_movie(movie_id: UUID, db: Session = Depends(get_db)):
    return get_movie_id(movie_id, db)

@router.get("/{movie_id}/language")
def view_language_of_movie(movie_id: UUID, db: Session = Depends(get_db)):
    return get_languages_by_movie(movie_id, db)


# theater admin 
@router.post("/")
def add_movie( movie : MovieCreate,db: Session =Depends(get_db),  current_user = Depends(require_role(["theater_admin", "admin"]))):
    return create_movie(movie,db)

@router.patch("/{movie_id}")
def update_movie_details(movie_id:UUID, movie: MovieUpdate,db: Session =Depends(get_db),  current_user = Depends(require_role(["theater_admin", "admin"]))):
    return movie_update(movie_id,movie,db)

@router.delete("/{movie_id}")
def remove_movie(movie_id: UUID, db: Session =Depends(get_db),  current_user = Depends(require_role(["theater_admin", "admin"]))):
    return delete_movie(movie_id,db)

@router.patch("/{movie_id}/activate")
def restore_movie(movie_id: UUID, db: Session = Depends(get_db),  current_user =Depends(require_role(["theater_admin", "admin"]))):
    return activate_movie(movie_id, db)

#language
@router.post("/{movie_id}/assign")
def assign_languages(movie_id: UUID, assignment: MovieLanguageAssignment, db: Session =Depends(get_db),  current_user = Depends(require_role(["theater_admin", "admin"]))):
    return assign_languages_to_movie(movie_id, assignment, db)

@router.delete("/{movie_id}/remove/{language_id}")
def remove_language_movie(movie_id: UUID, language_id: UUID, db: Session =Depends(get_db),  current_user = Depends(require_role(["theater_admin", "admin"]))):
    return remove_language_from_movie(movie_id, language_id, db)
