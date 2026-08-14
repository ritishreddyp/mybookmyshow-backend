from fastapi import Depends,FastAPI
from sqlalchemy.orm import Session

from config import  engine,Base,sessionlocal
from config_models.user import user

app = FastAPI()

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

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(user).all()

@app.get("/users/{user_id}")
def get_user_by_id(user_id:int,db: Session = Depends(get_db)):
    user = db.query(user).filter(user.user_id == user_id).first()
    return user 

