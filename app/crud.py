from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import SQUser
from app.schemas.user import UserCreate, UserLogin, UserUpdate,UserDetails

from app.models.city import SQcity
from app.schemas.city import CityCreate, CityUpdate,CityDetails

from app.models.movies import SQmovies
from app.schemas.movies import MovieCreate,MovieUpdate,MovieDetails



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
def movie_update(movie_id: int, movie: MovieUpdate, db: Session) -> SQmovies:
    existing_movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()
    if not existing_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Movie not found")

    update_data  = movie.model_dump(exclude_unset=True)



    new_title = update_data.get("title", existing_movie.title)
    new_release_date = update_data.get("release_date", existing_movie.release_date)

    if "title" in update_data or "release_date" in update_data:
        duplicate_movie = db.query(SQmovies).filter(SQmovies.title == new_title,SQmovies.release_date == new_release_date,SQmovies.movie_id != movie_id).first()

        if duplicate_movie:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="A movie with this title and release date already exists")


    for field, value in update_data.items():
        setattr(existing_movie, field, value)

    try:

        db.commit()
        db.refresh(existing_movie)

        return existing_movie
    
    except Exception:

        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Failed to update movie details")