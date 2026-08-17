from fastapi import Depends, FastAPI, HTTPException, status


from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from config import  engine,Base,sessionlocal

from config_models.user import SQUser
from models.user import User,UserUpdate

from config_models.city import SQcity
from models.city import City

from config_models.movies import SQmovies
from models.movies import movies

app = FastAPI()

password_hash = PasswordHash.recommended()


Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return " Welcome To MyBookMyShow "



#---------------------------------------------------------•	User Registration Mangement-------------------------------------------------------------#

#----------------To create new user----------------#

@app.post("/users/register")
def create_new_user(user:User,db: Session = Depends(get_db)): 

    already_user = db.query(SQUser).filter((SQUser.email == user.email)|(SQUser.phone_number == user.phone_number)).first()

    if already_user:

        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = password_hash.hash(user.password)

    new_user = SQUser(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password)

    db.add(new_user)
    db.commit()

    return " User successfully registered "


#--------------------user login---------------#

@app.get("/users/login")
def login_user(credentials: User, db: Session = Depends(get_db)):

    user = db.query(SQUser).filter(SQUser.email == credentials.email).first()
    
    if not user or not password_hash.verify(credentials.password, user.password):

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    return  "Login successful"


#--------------update user details------------#

@app.patch("/users/{user_id}/update")
def update_user_details(user_id:int,user:UserUpdate,db: Session = Depends(get_db)):

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


#---------------delete user details-------------#

@app.delete("/users/{user_id}/delete")
def delete_user(user_id:int,db: Session = Depends(get_db)):

    existing_user = db.query(SQUser).filter(SQUser.user_id == user_id).first()

    if not  existing_user:
            raise HTTPException( status_code=404, detail = "User not found" )

    
    db.delete(existing_user)
    db.commit()

    return "user deleted sucessfully"

#--------------------------------------------------------Movies Management -----------------------------------------------------------#

# City user operations to view and select city 

@app.get("/city")
def get_all_cities(db: Session = Depends(get_db)):
    return db.query(SQcity).all()

@app.get("/city/{city_id}")
def get_city_id(city_id:int,db: Session = Depends(get_db)):
    cities = db.query(SQcity).filter(SQcity.city_id == city_id).first()

    if cities is None:
        raise HTTPException(status_code=404, detail="City not found")
    return cities


# City Admin operations to add and delete city

@app.post("/city")
def add_city(city:City,db: Session = Depends(get_db)):
    existing_city =db.query(SQcity).filter((SQcity.city_name == city.city_name)).first()
    if existing_city:
        raise HTTPException(status_code=400,detail="city already exists")
    new_city = SQcity(city_name=city.city_name,state=city.state)

    db.add(new_city)
    db.commit()
    return " city added successfully"


# Movies User operations
# To view all movies in city  

@app.get("/cities/{city_id}/movies", summary="Get all movies playing in a city")
def get_movies_by_city(city_id: int, db: Session = Depends(get_db)):

    city = db.query(SQcity).filter(SQcity.city_id == city_id).first()

    if not city:

        raise HTTPException(status_code=404, detail="City not found")
    
    return [movie for movie in city.movies if movie.status == "active"]


# To view one movie details in movies section


@app.get("/movies/{movie_id}", summary="Get detailed view of a specific movie")
def get_movie_details(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(SQmovies).filter(SQmovies.movie_id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie




# Movies Admin operations 
# To add , delete , update movie details






