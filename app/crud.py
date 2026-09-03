from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List
import uuid
from pathlib import Path


from app.models.user import SQUser
from app.schemas.user import UserCreate, UserLogin, UserUpdate,UserDetails

from app.models.city import SQcity
from app.schemas.city import CityCreate, CityUpdate,CityDetails

from app.models.movies import SQmovies
from app.schemas.movies import MovieCreate,MovieUpdate,MovieDetails

from app.models.languages import SQlanguages
from app.schemas.languages import LanguageCreate,LanguageDetails,LanguageUpdate,MovieLanguageAssignment

from app.models.theatres import SQtheaters
from app.schemas.theatres import TheatreCreate,TheatreUpdate,TheatreDetails

from app.models.screens import SQscreens
from app.schemas.screens import ScreenCreate,ScreenUpdate,ScreenDetails

from app.models.seats import SQseats
from app.schemas.seats import SeatCreate

from app.models.shows import SQshows
from app.schemas.shows import ShowCreate, ShowUpdate

from app.models.show_seats import SQshow_seats
from app.schemas.show_seats import SeatBookingRequest


from app.models.booking_section import SQbooking_section
from app.models.booking_item import SQbooking_items
from app.schemas.booking_section import BookingCreate,BookingStatusUpdate,BookingSectionResponse
from app.schemas.booking_item import BookingItemAdd , BookingItemResponse

from app.models.payments import SQpayments
from app.schemas.payments import PaymentProcessRequest,PaymentDetails

from app.models.tickets import SQtickets
from app.schemas.tickets import TicketOut,BookingConfirmation

from app.core.security import password_hash



#------------------------------------------------------- user operations-----------------------------------------------------#
# user creation

def create_new_user(user: UserCreate, db: Session):  

    already_user = db.query(SQUser).filter((SQUser.email == user.email)|(SQUser.phone_number == user.phone_number)).first()

    if already_user:

        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = password_hash.hash(user.password)

    new_user = SQUser(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password,
        status="Active")

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise

    return " User successfully registered "

# Update user details

def update_user_details(user_id: int, user: UserUpdate, db: Session):

    existing_user =db.query(SQUser).filter(SQUser.user_id == user_id).first()

    if not existing_user:
        raise HTTPException(status_code=404,detail="User not found")

    update_user = user.model_dump(exclude_unset=True)

    if "username" in update_user:
        existing_username =db.query(SQUser).filter(SQUser.username == update_user["username"],SQUser.user_id != user_id).first()

        if existing_username:
            raise HTTPException(status_code=400,detail="Username already exists")

        existing_user.username = update_user["username"]

    
    if "email" in update_user:
        existing_email = db.query(SQUser).filter(SQUser.email == update_user["email"],SQUser.user_id != user_id).first()

        if existing_email:
            raise HTTPException(status_code=400,detail="Email already exists")

        existing_user.email = update_user["email"]


    if "phone_number" in update_user:
        existing_phone = db.query(SQUser).filter(SQUser.phone_number == update_user["phone_number"],SQUser.user_id != user_id).first()

        if existing_phone:
            raise HTTPException(status_code=400,detail="Phone number already exists")

        existing_user.phone_number = update_user["phone_number"]

    if "password" in update_user:
        same_password = password_hash.verify(update_user["password"], existing_user.password)
        if same_password:
            raise HTTPException(status_code=400, detail="new password can't be same as old password")

        existing_user.password = password_hash.hash(update_user["password"])

    db.commit()

    return "user details updated sucessfully"

# delete user details 

def delete_user(user_id: int, db: Session):

    existing_user = db.query(SQUser).filter(SQUser.user_id == user_id).first()

    if not  existing_user:
            raise HTTPException( status_code=404, detail = "User not found" )

    
    db.delete(existing_user)
    db.commit()

    return "user deleted sucessfully"

# get all users
#  
def get_all_users(db: Session):
    user = db.query(SQUser).all()

    return user

#get user by id

def get_user_id(user_id : int, db: Session):
    user_detail = db.query(SQUser).filter(SQUser.user_id == user_id).first()
    if user_id is None:
                raise HTTPException(status_code=404, detail="Usern ot found")
    
    return user_detail


#---------------------------------------------------------- city operations ---------------------------------------------------------#

# get city details

def get_all_cities(db: Session):
    return db.query(SQcity).filter(SQcity.is_active == True).all()

# Get one city 

def get_city_id(city_id: int, db: Session):
    cities = db.query(SQcity).filter(SQcity.city_id == city_id).first()
    if cities is None:
            raise HTTPException(status_code=404, detail="City not found")
    return cities

# add city 

def create_city(city: CityCreate, db: Session):
    existing_city =db.query(SQcity).filter((SQcity.city_name == city.city_name)).first()
    if existing_city:
        raise HTTPException(status_code=400,detail="city already exists")
    new_city = SQcity(city_name=city.city_name,state=city.state)

    db.add(new_city)
    db.commit()
    return " city added successfully"

  
# delete city 

def delete_city(city_id: int, db: Session):
    city = db.query(SQcity).filter(SQcity.city_id == city_id).first()

    if not city:
            raise HTTPException(status_code=404, detail="City not found")

    city.is_active = False
    db.commit()

    return " city deleted succesfully "

#to get inactive city
def get_inactive_cities(db: Session):
    return db.query(SQcity).filter(SQcity.is_active == False).all()

# to update inactive city
def restore_city(city_id: int, db: Session):
    city = db.query(SQcity).filter(SQcity.city_id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    city.is_active = True
    db.commit()
    db.refresh(city)
    return "City activated successfully"

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

#  to ge inactive

def get_inactive_languages(db: Session):
    return db.query(SQlanguages).filter(SQlanguages.is_active == False).all()

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

# remove language
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

# to get inactive languages
def activate_language(language_id: int, db: Session):
    lang = db.query(SQlanguages).filter(SQlanguages.language_id == language_id).first()
    if not lang:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Language not found")
    lang.is_active = True
    db.commit()
    return "Language activated successfully"


# -----------------------------------------------------------theaters-------------------------------------------------------------- 

# create theaters 
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
# update theaters
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

#get all theaters
def get_all_theaters(city_id: int | None, db: Session):
    query = db.query(SQtheaters).filter(SQtheaters.is_active == True)
    if city_id:
        query = query.filter(SQtheaters.city_id == city_id)
    return query.all()

# to get inactive theaters
def get_inactive_theaters(db: Session):
    return db.query(SQtheaters).filter(SQtheaters.is_active == False).all()

# get theater by id

def get_theater_by_id(theater_id: int, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")
    return theater

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


#-------------------------------------------------------screens---------------------------------------------------

# add theater to screen 

def add_screen_to_theater(theater_id: int, screen_name: str, screen_type: str, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")

    max_id = db.query(func.max(SQscreens.screen_id)).filter(SQscreens.theater_id == theater_id).scalar()
    next_screen_id = (max_id or 0) + 1

    new_screen = SQscreens(
        theater_id=theater_id,
        screen_id=next_screen_id,  
        screen_name=screen_name,
        screen_type=screen_type,
        status="active"
    )
    
    try:

        db.add(new_screen)
        db.commit()
        db.refresh(new_screen)

    except Exception as e:

        db.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to add screen: {e}")

    return "Screen added successfully"

# get screens in theater

def get_screens_by_theater(theater_id: int, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")
    return [screen for screen in theater.screens if screen.is_active]


# Update Screens

def update_screen(screen_id: int, screen_update: ScreenUpdate, db: Session):
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

def delete_screen(screen_id: int, db: Session):
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

#to get inactive screens
def get_inactive_screens_by_theater(theater_id: int, db: Session):
    theater = db.query(SQtheaters).filter(SQtheaters.theater_id == theater_id).first()
    if not theater:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Theater not found")
    return [screen for screen in theater.screens if not screen.is_active]

# to activate screens
def activate_screen(screen_id: int, db: Session):
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

#-------------------------------------------------------------seats-------------------------------------------------------------#
def generate_seats_for_screen(hall: SeatCreate, db: Session):
    screen = db.query(SQscreens).filter(SQscreens.theater_id == hall.theater_id,SQscreens.screen_id == hall.screen_id).first()

    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found in theater")

    new_seats = []
    local_seat_counter = 1 

    for row in hall.rows:
        for seat_num in range(1, hall.seats_per_row + 1):
            seat_number_str = f"{row}{seat_num}"

            seat = SQseats(
                theater_id=hall.theater_id,
                screen_id=screen.id,
                seat_id=local_seat_counter,      
                seat_row=row,
                seat_number=seat_number_str,     
                seat_type=hall.seat_type)
            
            new_seats.append(seat)
            local_seat_counter += 1            

    try:

        db.add_all(new_seats)
        db.commit()

    except Exception as e:
        db.rollback()

        raise HTTPException( status.HTTP_500_INTERNAL_SERVER_ERROR,  detail=f"Failed to generate seats: {e}")

    return "Successfully generated local seats for screen"


def update_seats_for_screen(theater_id: int, screen_id: int, new_seat_type: str, db: Session):
    screen = db.query(SQscreens).filter(SQscreens.theater_id == theater_id,SQscreens.screen_id == screen_id).first()
    
    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found in this theater")

    updated_count = db.query(SQseats).filter(SQseats.screen_id == screen.id).update({SQseats.seat_type: new_seat_type},  synchronize_session=False )
    
    try:
        db.commit()

    except Exception as e:
        db.rollback()

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update screen seats: {e}" )

    return f"Successfully updated {updated_count} seats to '{new_seat_type}' for screen {screen_id}"


def delete_seats_for_screen(theater_id: int, screen_id: int, db: Session):
    screen = db.query(SQscreens).filter(    SQscreens.theater_id == theater_id,  SQscreens.screen_id == screen_id).first()
    
    if not screen:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Screen not found in this theater")

    deleted_count = db.query(SQseats).filter(SQseats.screen_id == screen.id).delete()
    
    try:
        db.commit()

    except Exception as e:
        db.rollback()

        raise HTTPException( status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete seats for screen: {e}" )

    return f"Successfully deleted {deleted_count} seats for screen {screen_id}"


#----------------------------------------------------shows---------------------------------------------------------------

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

    new_show = SQshows(
        movie_id=show.movie_id,
        screen_id=screen.id,
        language_id=show.language_id,
        show_date=show.show_date,
        show_time=show.show_time,
        base_price=show.base_price,
        status="active" )

    try:
        db.add(new_show)
        db.commit()
        db.refresh(new_show)

        generate_show_seats_for_show(show_id=new_show.show_id, screen_id=screen.id,  base_price=show.base_price, db=db)


    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create show: {e}")

    return "Show scheduled successfully"

# update show details

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

    query = db.query(SQshows).join(SQscreens, SQshows.screen_id == SQscreens.id).join(SQtheaters, SQscreens.theater_id == SQtheaters.theater_id)

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

#--------------------------------------------------------show_seats----------------------------------------------------
# to genrate seats for show 
def generate_show_seats_for_show(show_id: int, screen_id: int, base_price: float, db: Session):
    physical_seats = db.query(SQseats).filter(SQseats.screen_id == screen_id).all()
    if not physical_seats:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Cannot schedule show: No physical seats found for this screen. Create screen seats first.")

    show_seats_list = [
        SQshow_seats(show_id=show_id,seat_id=seat.id,  price=base_price,status="available")
        for seat in physical_seats
    ]

    db.add_all(show_seats_list)
    db.commit()

# to view show seats 
def get_show_seats(show_id: int, db: Session):
    show = db.query(SQshows).filter(SQshows.show_id == show_id).first()
    if not show:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Show not found")
    
    now = datetime.now()

    expired_locks = db.query(SQshow_seats).filter(SQshow_seats.show_id == show_id,SQshow_seats.status == "locked",SQshow_seats.lock_expires_at < now).all()
    for seat in expired_locks: 
        seat.status = "available" 
        seat.lock_expires_at = None
    
    if expired_locks:

        db.commit()

    show_seats_data = db.query(SQshow_seats, SQseats).join( SQseats, SQshow_seats.seat_id == SQseats.id).filter(SQshow_seats.show_id == show_id).all()

    if not show_seats_data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No seats found for this show. Ensure physical seats exist for this screen before scheduling." )
    
    result = []

    for ss, seat in show_seats_data:
        if ss.status == "available":
            availability_text = "available to book"
        elif ss.status == "locked":
            availability_text = "currently locked (temporary hold)"
        else:
            availability_text = "already booked"

        result.append({
            "show_seat_id": ss.show_seat_id,
            "show_id": ss.show_id,
            "seat_id": ss.seat_id,
            "row_name": seat.seat_row,
            "seat_number": seat.seat_number, 
            "seat_type": seat.seat_type,    
            "price": ss.price,
            "status": ss.status,
            "description": f"Seat {seat.seat_row}{seat.seat_number} is {availability_text}"
        })

    return result


# Select show seats  

def select_seats_and_create_summary(booking_data, current_user_id, db):
    show = db.query(SQshows).filter(SQshows.show_id == booking_data.show_id).first()
    if not show:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Show not found")
    
    seats = db.query(SQshow_seats).filter( SQshow_seats.show_id == booking_data.show_id,SQshow_seats.show_seat_id.in_(booking_data.seat_ids) ).all()

    if len(seats) != len(booking_data.seat_ids):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="One or more selected seats are invalid for this show.")

    for seat in seats:

        if seat.status != "available":
            raise HTTPException(status.HTTP_400_BAD_REQUEST,   detail=f"Seat ID {seat.show_seat_id} is currently {seat.status} and cannot be selected.")


    lock_expiration_time = datetime.now() + timedelta(minutes=10)

    for seat in seats:
        seat.status = "locked"
        seat.lock_expires_at = lock_expiration_time


    new_booking = SQbooking_section(user_id=current_user_id, show_id=booking_data.show_id,booking_status="Pending",total_amount=sum(seat.price for seat in seats))

    db.add(new_booking)
    db.flush() 

    booking_items = []

    for seat in seats:
        item = SQbooking_items(booking_id=new_booking.booking_id,show_seat_id=seat.show_seat_id,price=seat.price )
        db.add(item)
        booking_items.append(item)

    db.commit()
    db.refresh(new_booking)
    
    return {
        "message": "Order summary created successfully! Seats are temporarily locked for 10 minutes.",
        "booking_id": new_booking.booking_id,
        "show_id": new_booking.show_id,
        "booking_status": new_booking.booking_status,
        "total_amount": new_booking.total_amount,
        "lock_expires_at": lock_expiration_time,
        "items": [
            {"booking_item_id": item.booking_item_id, "show_seat_id": item.show_seat_id, "price": item.price} 
            for item in booking_items]
    }


# modify booking items
def delete_booking_item(booking_id: int, booking_item_id: int, current_user_id: int, db: Session):
    booking = db.query(SQbooking_section).filter(SQbooking_section.booking_id == booking_id,SQbooking_section.user_id == current_user_id).first()
    if not booking:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Booking section not found or unauthorized.")

    if booking.booking_status != "Pending":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Cannot modify items for a non-pending booking.")


    item = db.query(SQbooking_items).filter(SQbooking_items.booking_item_id == booking_item_id,SQbooking_items.booking_id == booking_id ).first()
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Booking item not found in this order.")

    show_seat = db.query(SQshow_seats).filter(SQshow_seats.show_seat_id == item.show_seat_id).first()
    if show_seat:
        show_seat.status = "available"
        show_seat.lock_expires_at = None

    item_price = item.price
    db.delete(item)
    db.flush()

    booking.total_amount -= item_price
    if booking.total_amount <= 0:
        booking.booking_status = "Cancelled"

    db.commit()

    return  {"message": "Booking item removed successfully. Seat lock released.","booking_id": booking.booking_id,"new_total_amount": booking.total_amount}


# ================================================= payments =============================================================

# To ger all user bookings

def get_user_booking(booking_id: int, user_id: int, db: Session):
    booking = db.query(SQbooking_section).filter_by(booking_id=booking_id, user_id=user_id).first()
    if not booking:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Booking not found.")
    return booking

# payment checkout
def get_checkout_summary(booking_id: int, user_id: int, db: Session):
    booking = get_user_booking(booking_id, user_id, db)
    items = db.query(SQbooking_items).filter_by(booking_id=booking_id).all()
    seats = db.query(SQshow_seats).filter(SQshow_seats.show_seat_id.in_([i.show_seat_id for i in items])).all()

    if any(s.lock_expires_at and s.lock_expires_at < datetime.now() for s in seats):

        for s in seats: s.status, s.lock_expires_at = "available", None
        booking.booking_status = "Expired"

        db.commit()

        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Checkout session expired.")

    ticket_price = sum(i.price for i in items)

    convenience_fees = round(ticket_price * 0.1015, 2), 2.0

    booking.total_amount = round(ticket_price + convenience_fees , 2)

    db.commit()

    return {
        "booking_id": booking.booking_id, "show_id": booking.show_id, "booking_status": booking.booking_status,
        "pricing_breakdown": {"ticket_price": ticket_price, "convenience_fees": convenience_fees, "order_total": booking.total_amount},
        "seats_count": len(items), "lock_expires_at": seats[0].lock_expires_at if seats else None}

# payment methods
PAYMENT_CATEGORIES = {
    "upi": {
        "id": "upi",
        "name": "Pay by any UPI App",
        "options": ["Scan QR Code", "GPay", "PhonePe", "Paytm"]
    },
    "cards": {
        "id": "cards",
        "name": "Debit/Credit Card",
        "options": ["Visa", "Mastercard", "RuPay"]
    },
    "wallets": {
        "id": "wallets",
        "name": "Mobile Wallets",
        "options": ["Paytm", "Amazon Pay", "Mobikwik"]
    },
    "net_banking": {
        "id": "net_banking",
        "name": "Net Banking",
        "options": ["HDFC", "ICICI", "SBI", "Axis"]
    },
    "pay_later": {
        "id": "pay_later",
        "name": "Pay Later",
        "options": ["Simpl", "LazyPay"]
    }
}
# to view methods
def get_payment_methods():
    return {"payment_categories": list(PAYMENT_CATEGORIES.values())}
# to select method

def select_payment_method(category_id: str):
    category = PAYMENT_CATEGORIES.get(category_id.strip().lower())
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment method '{category_id}' not found. Available options: {list(PAYMENT_CATEGORIES.keys())}" )
    return {
        "message": f"Payment method '{category['name']}' selected successfully.",
        "selected_category": category,
        "next_step": "Proceed to POST /payments/initiate with booking_id and payment_method"
    }


#payment intiation
def initiate_payment(payload: PaymentProcessRequest, user_id: int, db: Session):
    booking = get_user_booking(payload.booking_id, user_id, db)
    if booking.booking_status != "Pending":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Booking is not pending.")

    txn_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
    payment = SQpayments(booking_id=booking.booking_id, transaction_id=txn_id, payment_method=payload.payment_method, amount=booking.total_amount, payment_status="Processing")

    db.add(payment)
    db.commit()

    return {
        "payment_id": payment.payment_id, "booking_id": booking.booking_id, "transaction_id": txn_id,
        "payable_amount": payment.amount, "payment_status": payment.payment_status,
        "upi_qr_payload": f"upi://pay?pa=bookmyshow@icici&pn=BookMyShow&am={booking.total_amount}&tr={txn_id}&cu=INR" if payload.payment_method.upper() == "UPI" else None}


#  confirm booking
def verify_and_confirm_payment(booking_id: int, transaction_id: str, user_id: int, db: Session):
    booking = get_user_booking(booking_id, user_id, db)
    payment = db.query(SQpayments).filter_by(booking_id=booking_id, transaction_id=transaction_id).first()
    if not payment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Payment transaction not found.")


    items = db.query(SQbooking_items).filter_by(booking_id=booking_id).all()
    seats = db.query(SQshow_seats).filter(SQshow_seats.show_seat_id.in_([i.show_seat_id for i in items])).all()
    if any(s.lock_expires_at and s.lock_expires_at < datetime.now() for s in seats):
        payment.payment_status, booking.booking_status = "Failed", "Expired"

        for s in seats: s.status, s.lock_expires_at = "available", None
        db.commit()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Payment failed: Lock timer expired.")


    for seat in seats:
        seat.status = "booked"
        seat.lock_expires_at = None

    payment.payment_status, booking.booking_status = "Success", "Confirmed"
    ticket = SQtickets(booking_id=booking.booking_id, show_id=booking.show_id, ticket_code=f"BMS-TKT-{uuid.uuid4().hex[:8].upper()}", ticket_status="Confirmed")

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    db.refresh(payment)

    return {"booking_id": booking.booking_id, "total_amount": booking.total_amount, "booking_status": booking.booking_status, "ticket": ticket, "payment": payment}


# -------------------------------------------------------tickets -------------------------------------------------
# genrate tickets
def get_ticket_details(booking_id: int, user_id: int, db: Session):
    booking = get_user_booking(booking_id, user_id, db)
    ticket = db.query(SQtickets).filter_by(booking_id=booking_id).first()
    payment = db.query(SQpayments).filter_by(booking_id=booking_id).first()

    if not ticket:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="M-Ticket not found for this booking.")
    
    return {"booking_id": booking.booking_id, "total_amount": booking.total_amount, "booking_status": booking.booking_status, "ticket": ticket, "payment": payment}