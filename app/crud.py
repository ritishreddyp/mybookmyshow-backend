from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import SQUser
from app.models.city import SQcity

from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.schemas.city import CityCreate, CityUpdate,CityDetails

from app.core.security import password_hash


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
        password=hashed_password)

    db.add(new_user)
    db.commit()

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

def add_city(city: CityCreate, db: Session):
    existing_city =db.query(SQcity).filter((SQcity.city_name == city.city_name)).first()
    if existing_city:
        raise HTTPException(status_code=400,detail="city already exists")
    new_city = SQcity(city_name=city.city_name,state=city.state)

    db.add(new_city)
    db.commit()
    return " city added successfully"


