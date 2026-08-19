from fastapi import Depends ,HTTPException ,status
from fastapi.security import OAuth2PasswordBearer

from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.config import settings
from app.core.security import decode_access_token
from app.models.user import SQUser


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)) -> SQUser:

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