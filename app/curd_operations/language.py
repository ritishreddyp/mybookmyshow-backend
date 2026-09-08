from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.languages import SQlanguages
from app.schemas.languages import LanguageCreate,LanguageUpdate,MovieLanguageAssignment

from app.models.movies import SQmovies


#---------------------------------------------------------------langauges -----------------------------------------------------
# add language 
def create_language(language: LanguageCreate, db: Session):
    if db.query(SQlanguages).filter_by(language_name=language.language_name).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Language already exists")

    new_lang = SQlanguages(language_name=language.language_name, status="available", is_active=True)

    try:
        db.add(new_lang)
        db.commit()
        db.refresh(new_lang)

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed: {e}")
    
    return "Language added successfully"


# update language 
def update_language(language_id: int, language: LanguageUpdate, db: Session):
    lang = db.query(SQlanguages).filter(SQlanguages.language_id == language_id).first()
    if not lang:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Language not found")

    update_data = language.model_dump(exclude_unset=True)
    
    if "language_name" in update_data:
        duplicate = db.query(SQlanguages).filter( SQlanguages.language_name == update_data["language_name"], SQlanguages.language_id != language_id).first()
        if duplicate:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Language already exists")

    for key, value in update_data.items():
        setattr(lang, key, value)

    try:
        db.commit()
        db.refresh(lang)

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed: {e}")
        
    return "Language updated successfully"


# assign language to movie 
def assign_languages_to_movie(movie_id: int, assignment: MovieLanguageAssignment, db: Session):
    movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")

    languages = db.query(SQlanguages).filter(SQlanguages.language_id.in_(assignment.language_ids),SQlanguages.is_active == True).all()

    if len(languages) != len(assignment.language_ids):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "One or more language IDs not found")

    added = False
    for lang in languages:
        if lang not in movie.languages:
            movie.languages.append(lang)
            added = True

    if not added:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Selected languages are already assigned to this movie")

    try:
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed: {e}")
        
    return "Languages assigned to movie successfully"


# remove language from  movie
def remove_language_from_movie(movie_id: int, language_id: int, db: Session):
    movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()
    lang = db.query(SQlanguages).filter(SQlanguages.language_id == language_id).first()

    if not movie or not lang:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie or Language not found")

    if lang not in movie.languages:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Language is not assigned to this movie")

    movie.languages.remove(lang)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed: {e}")
        
    return "Language removed from movie successfully"


# select language to view all movies in selected language
def get_movies_by_language(language_id: int, db: Session):
    lang = db.query(SQlanguages).filter(SQlanguages.language_id == language_id, SQlanguages.is_active == True).first()
    if not lang:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Language not found")
    
    return lang.movies


#  view all available languages of selected movie 
def get_languages_by_movie(movie_id: int, db: Session):
    movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
    
    return  [lang for lang in movie.languages if lang.is_active]


# to remove or deactivate language
def delete_language(language_id: int, db: Session):
    lang = db.query(SQlanguages).filter(SQlanguages.language_id == language_id).first()
    if not lang:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Language not found")

    try:
        lang.is_active = False
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed: {e}")
        
    return "Language deleted successfully"


#  to ge inactive
def get_inactive_languages(db: Session):
    return db.query(SQlanguages).filter(SQlanguages.is_active == False).all()


# to activate languages
def activate_language(language_id: int, db: Session):
    lang = db.query(SQlanguages).filter(SQlanguages.language_id == language_id).first()
    if not lang:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Language not found")
    lang.is_active = True

    db.commit()
    return "Language activated successfully"
