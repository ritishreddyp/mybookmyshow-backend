from pydantic import BaseModel, EmailStr

#admins 
class MainAdminProvisionCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

#admin password modification
class AdminPasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str