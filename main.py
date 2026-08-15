from fastapi import Depends,FastAPI,HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash


from config import  engine,Base,sessionlocal
from config_models.user import SQUser
from models.user import User,UserUpdate


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
    return "MyBookMyShow"

#=====================================user operations=============================================#

#=========get all users=========#

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(SQUser).all()


#=========get user by id=========#


@app.get("/users/{user_id}")
def get_user_by_id(user_id:int, db: Session = Depends(get_db)):

    user = db.query(SQUser).filter(SQUser.user_id == user_id).first()
    if user is None:
        raise HTTPException( status_code=404, detail = "User not found" )
    return user 


#=========create new user========#

@app.post("/users")
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

#==============update user details=========#

@app.patch("/users/{user_id}")
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

#======delete user details=======#

@app.delete("/users/{user_id}")
def delete_user(user_id:int,db: Session = Depends(get_db)):

    existing_user = db.query(SQUser).filter(SQUser.user_id == user_id).first()

    if not  existing_user:
            raise HTTPException( status_code=404, detail = "User not found" )
    db.delete(existing_user)
    db.commit()
    return "user deleted sucessfully"