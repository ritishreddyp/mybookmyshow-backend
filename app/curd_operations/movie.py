from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pathlib import Path


from app.models.movies import SQmovies
from app.schemas.movies import MovieCreate,MovieUpdate,MovieDetails
#---------------------------------------------------- movies operations ------------------------------------------------------------#

# add movie 
def create_movie(movie: MovieCreate , db:Session):

    existing_movie= db.query(SQmovies).filter(SQmovies.title == movie.title,SQmovies.release_date == movie.release_date ).first()
    if existing_movie:
         raise HTTPException(status_code=400,detail="Movie already exists")
    
    new_movie = SQmovies(title= movie.title,description= movie.description,genre= movie.genre,duration_minutes= movie.duration_minutes,release_date= movie.release_date,poster_url= movie.poster_url,status= movie.status) 

    db.add(new_movie)
    db.commit()

    return " movie added succesfully"


# update movie
def movie_update(movie_id: int, movie: MovieUpdate, db: Session):
    existing_movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()
    if not existing_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="movie not found" )

    update_data = movie.model_dump(exclude_unset=True)
    new_title = update_data.get("title", existing_movie.title)
    new_release_date = update_data.get("release_date", existing_movie.release_date)

    if "title" in update_data or "release_date" in update_data:
        duplicate_movie = db.query(SQmovies).filter(
            SQmovies.title == new_title,
            SQmovies.release_date == new_release_date,
            SQmovies.movie_id != movie_id).first()

        if duplicate_movie:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="A movie with this title and release date already exists")

    for field, value in update_data.items():
        setattr(existing_movie, field, value)

    try:

        db.commit()
        db.refresh(existing_movie)
        return " Movie details updated sucessfully "
    
    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update movie details: {str(e)}" )

    
#movie delete
def delete_movie(movie_id: int, db: Session):
    movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()
    if not movie:
            raise HTTPException(status_code=404, detail="City not found")

    movie.is_active = False
    db.commit()

    return " movie deleted succesfully "


#to activate movie
def activate_movie(movie_id: int, db: Session):
    movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.is_active = True
    db.commit()
    return  "Movie activated successfully"


# to get all active movies
def get_active_movies(db: Session):
    return db.query(SQmovies).filter(SQmovies.is_active == True).all()


# veiw one movie
def get_movie_id(movie_id : int, db: Session):
    movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()

    if movie_id is None:
                raise HTTPException(status_code=404, detail="movie ot found")
    if not movie.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Movie is inactive")

    movie_folder = Path(r"C:\Users\HP\OneDrive\Documents\movie_images") / f"movie_{movie_id}"
    image_urls = []
    
    if movie_folder.exists():
        image_urls = [f"/images/movie_{movie_id}/{img.name}" for img in movie_folder.iterdir() if img.is_file()]
        movie_details = {
        "movie_id": movie.movie_id,
        "title": movie.title,
        "description": movie.description,
        "genre": movie.genre,
        "duration_minutes": movie.duration_minutes,
        "release_date": movie.release_date,
        "poster_url": movie.poster_url,
        "status": movie.status,
        "is_active": movie.is_active,
        "images": image_urls
    }
    return movie_details


# to get view inactive movies
def get_inactive_movies(db: Session):
    return db.query(SQmovies).filter(SQmovies.is_active == False).all()

