from fastapi import Depends,HTTPException ,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.db import get_db
from app.core.config import settings
from app.core.security import decode_access_token
from app.models.user import SQUser
from app.models.admin import SQMainAdmin
from app.models.theater_admin import SQTheaterAdmin


security = HTTPBearer(auto_error=False)


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security), db: Session = Depends(get_db)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication credentials were not provided")
    
    try:
        payload = decode_access_token(credentials.credentials)
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if not email or not role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate your credentials")

    if role == "admin":
        user = db.query(SQMainAdmin).filter(SQMainAdmin.email == email).first()
    elif role == "theater_admin":
        user = db.query(SQTheaterAdmin).filter(SQTheaterAdmin.email == email).first()
    else:
        user = db.query(SQUser).filter(SQUser.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    setattr(user, "role", role)
    if role == "theater_admin":
        setattr(user, "theater_id", payload.get("theater_id"))

    return user


def require_role(allowed_roles: List[str]):
    def role_checker(current_user = Depends(get_current_user)):

        user_role = getattr(current_user, "role", None)
        if user_role == "admin":
            return current_user
        
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access forbidden: Requires one of {allowed_roles}")

        return current_user
    return role_checker