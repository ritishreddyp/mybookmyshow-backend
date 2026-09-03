from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.user import UserLogin
from app.core.security import verify_password, create_access_token
from app.models.user import SQUser

router = APIRouter()


@router.post("/login")
def user_login(credentials: UserLogin , db: Session = Depends(get_db)):
    user = db.query(SQUser).filter(SQUser.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"}, )

    access_token = create_access_token(subject=user.email)
    
    return { "access_token": access_token, "token_type": "bearer" }
