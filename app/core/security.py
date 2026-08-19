from datetime import datetime , timezone ,timedelta
from pwdlib import PasswordHash

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings


password_hash = PasswordHash.recommended()


#password hashing 
def get_password_hash(password: str) -> str:

    return password_hash.hash(password)

#password verification
def verify_password(plain_password: str, hashed_password: str) -> bool:

    return password_hash.verify(plain_password, hashed_password)



#jwt creation
def create_access_token(subject: str | int, expires_delta: timedelta | None = None) -> str:

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_TIME))

    payload = {
        "sub": str(subject),
        "exp": expire}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


#jwt decoding
def decode_access_token(token: str) -> dict:

    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])