from datetime import datetime , timezone ,timedelta
from pwdlib import PasswordHash
from app.core.config import settings
from typing import Optional
import jwt

import re
from fastapi import HTTPException, status

password_hash = PasswordHash.recommended()


#password hashing 
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


#password verification
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


#jwt creation
def create_access_token(email: str, role: str, theater_id: Optional[str] = None, expires_delta: timedelta | None = None) -> str:
    to_encode = {
        "sub": email,
        "email": email,
        "role": role,
        "theater_id": theater_id
    }
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


#jwt decoding
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


# assign role and scope based on email
def determine_role_and_scope(email: str):
    email = email.lower().strip()

    #admin
    if re.match(r"^[a-z0-9._%+-]+\.admin@mybookmyshow\.com$", email):
        return {"role": "admin", "theater_id": None}
    #theateradmin
    match = re.match(r"^([a-z0-9]+)\.theateradmin@mybookmyshow\.com$", email)
    if match:
        return {"role": "theater_admin", "theater_id": match.group(1)}
    
    if "mybookmyshow.com" in email:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=" Unauthorized Request " )
        
    return {"role": "public", "theater_id": None}
    