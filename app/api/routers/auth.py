from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.crud import create_new_user,login_user,update_user_details,delete_user
from app.schemas.user import UserCreate, UserLogin, UserUpdate

router = APIRouter()

@router.post("/login")
def user_login(credentials: UserLogin, db: Session = Depends(get_db)):
    return login_user(credentials, db)

