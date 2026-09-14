from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.db import get_db
from app.curd_operations.auth_operations import authenticate_customer,authenticate_main_admin,authenticate_theater_admin


router = APIRouter()

@router.post("/login/user")
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_customer(form_data.username, form_data.password, db)

@router.post("/login/admin")
def main_admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_main_admin(form_data.username, form_data.password, db)

@router.post("/login/theater-admin")
def theater_admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_theater_admin(form_data.username, form_data.password, db)
