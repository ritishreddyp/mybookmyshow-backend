from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

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

# user login 

def login_user(credentials: UserLogin, db: Session):

    user = db.query(SQUser).filter(SQUser.email == credentials.email).first()
    
    if not user or not password_hash.verify(credentials.password, user.password):

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    return  "Login successful"

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
    return db.query(SQcity).all()

# Get one city 

def get_city_id(city_id: int, db: Session):
    cities = db.query(SQcity).filter(SQcity.city_id == city_id).first()
    if cities is None:
            raise HTTPException(status_code=404, detail="City not found")
    return cities

# update city 

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

    db.delete(city)
    db.commit()

    return " city deleted succesfully "



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

    db.delete(movie)
    db.commit()

    return " movie deleted succesfully "


# to get all movies

def get_all_movies(db: Session):
    movies = db.query(SQmovies).all()

    return movies

# veiw one movie

def get_movie_id(movie_id : int, db: Session):
    movie_detail = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()
    if movie_id is None:
                raise HTTPException(status_code=404, detail="Usern ot found")
    
    return movie_detail


#---------------------------------------------------------------langauges -----------------------------------------------------
# add language 
def create_language(language: LanguageCreate, db: Session):
    if db.query(SQlanguages).filter_by(language_name=language.language_name).first():

        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Language already exists")

    new_lang = SQlanguages(language_name=language.language_name, status="available")

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

    languages = db.query(SQlanguages).filter(SQlanguages.language_id.in_(assignment.language_ids)).all()

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
    lang = db.query(SQlanguages).filter(SQlanguages.language_id == language_id).first()
    if not lang:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Language not found")
    return lang.movies

#  view all available languages of selected movie 
def get_languages_by_movie(movie_id: int, db: Session):
    movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
    return movie.languages

# remove language
def delete_language(language_id: int, db: Session):
    lang = db.query(SQlanguages).filter(SQlanguages.language_id == language_id).first()
    if not lang:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Language not found")

    try:
        db.delete(lang)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed: {e}")
        
    return "Language deleted successfully"



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
    query = db.query(SQtheaters)
    if city_id:
        query = query.filter(SQtheaters.city_id == city_id)
    return query.all()

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
    return theater.screens


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

        db.delete(screen)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete screen: {e}")

    return "Screen deleted successfully"



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
    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create show: {e}")

    return "Show scheduled successfully"

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