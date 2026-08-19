from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    username : str
    email : EmailStr
    phone_number : str
    password : str


class UserLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str = "bearer"


class UserDetails(BaseModel):
    user_id : int
    username : str
    email : EmailStr
    phone_number : str
    status : str
    created_at : datetime
    updated_at : datetime
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username : str |  None = None
    email : EmailStr |  None = None
    phone_number : str | None = None
    password : str | None = None