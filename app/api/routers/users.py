from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.crud import create_new_user,update_user_details,delete_user,get_all_users,get_user_id
from app.schemas.user import UserCreate, UserUpdate,UserDetails

router = APIRouter()


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(user, db)

@router.patch("/{user_id}")
def update_user(user_id: int,user: UserUpdate,db: Session = Depends(get_db)):
    return update_user_details(user_id, user, db)


@router.delete("/{user_id}")
def remove_user(user_id: int,db: Session = Depends(get_db)):
    return delete_user(user_id, db)

@router.get("/")
def get_users(db:Session = Depends(get_db)):
    return get_all_users(db)

@router.get("/{user_id}")
def get_user_by_id(user_id:int,db:Session = Depends(get_db)):
    return get_user_id(user_id,db)