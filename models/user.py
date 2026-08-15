from pydantic import BaseModel , EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str

#for updating password
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    password: str | None = None