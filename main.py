from fastapi import Depends,FastAPI,HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash



from config import  engine,Base,sessionlocal
from config_models.user import SQUser
from models.user import User


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









