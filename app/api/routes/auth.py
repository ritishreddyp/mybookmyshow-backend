from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.crud import create_new_user,login_user,update_user_details,delete_user
from app.schemas.user import UserCreate, UserLogin, UserUpdate

router = APIRouter()

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(user, db)

@router.post("/login")
def user_login(credentials: UserLogin, db: Session = Depends(get_db)):
    return login_user(credentials, db)

@router.patch("/{user_id}")
def update_user(user_id: int,user: UserUpdate,db: Session = Depends(get_db)):
    return update_user_details(user_id, user, db)


@router.delete("/{user_id}")
def remove_user(user_id: int,db: Session = Depends(get_db)):
    return delete_user(user_id, db)