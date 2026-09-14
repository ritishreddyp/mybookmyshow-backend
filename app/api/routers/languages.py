from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.api.deps import require_role

from app.curd_operations.language import create_language,assign_languages_to_movie,update_language,delete_language,get_languages_by_movie,get_movies_by_language,remove_language_from_movie, get_inactive_languages, activate_language
from app.schemas.languages import LanguageCreate,MovieLanguageAssignment,LanguageUpdate

router = APIRouter()

# public access
@router.get("/")
def get_languages(db: Session = Depends(get_db)):
    return {"message": "languages catalog"}

@router.get("/{language_id}/movies")
def view_movies_by_language(language_id: UUID, db: Session = Depends(get_db)):
    return get_movies_by_language(language_id, db)


# theater admin
@router.get("/inactive")
def list_inactive_languages(db: Session = Depends(require_role(["theater_admin", "admin"]))):
    return get_inactive_languages(db)

@router.patch("/{language_id}/activate")
def restore_language(language_id: UUID, db: Session = Depends(require_role(["theater_admin", "admin"]))):
    return activate_language(language_id, db)


# admin access
@router.post("/")
def add_language(language: LanguageCreate, db: Session = Depends((require_role(["admin"])))):
    return create_language(language, db)

@router.put("/{language_id}")
def edit_language(language_id: UUID, language: LanguageUpdate, db: Session = Depends((require_role(["admin"])))):
    return update_language(language_id, language, db)

@router.delete("/{language_id}")
def remove_language(language_id: UUID, db: Session = Depends(require_role(["admin"]))):
    return delete_language(language_id, db)