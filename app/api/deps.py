from fastapi import Depends ,HTTPException ,status
from fastapi.security import HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from typing import List


from app.core.db import get_db
from app.core.config import settings
from app.core.security import decode_access_token
from app.models.user import SQUser

security_scheme = HTTPBearer()

def get_current_user(db: Session = Depends(get_db),token: str = Depends(security_scheme)) -> SQUser:

    user_details_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"},)

    try:

        payload = decode_access_token(token)
        subject: str | None = payload.get("sub")

        if subject is None:

            raise user_details_exception
        
    except InvalidTokenError:

        raise user_details_exception
    
    user: SQUser | None = db.query(SQUser).filter(SQUser.email == subject).first()

    if user is None:
        
        raise user_details_exception

    return user

def require_roles(allowed_roles: List[str]):
    def role_checker(current_user: SQUser = Depends(get_current_user)) -> SQUser:
        user_role = current_user.role.name if getattr(current_user, "role", None) else "user"
        if user_role not in allowed_roles:

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access forbidden: Requires one of {allowed_roles}")
        
        return current_user
    
    return role_checker