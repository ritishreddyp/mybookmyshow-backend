from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.user import SQUser
from app.schemas.user import UserCreate, UserUpdate,UserDetails

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
def update_user_details(user_id: UUID, user: UserUpdate, db: Session):
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
def delete_user(user_id: UUID, db: Session):
    existing_user = db.query(SQUser).filter(SQUser.user_id == user_id).first()
    if not  existing_user:
            raise HTTPException( status_code=404, detail = "User not found" )


    db.delete(existing_user)
    db.commit()

    return "user deleted sucessfully"


# get all users
def get_all_users(db: Session):
    user = db.query(SQUser).all()

    return user


#get user by id
def get_user_id(user_id : UUID, db: Session):
    user_detail = db.query(SQUser).filter(SQUser.user_id == user_id).first()
    if user_id is None:
                raise HTTPException(status_code=404, detail="Usern ot found")
    
    return user_detail
