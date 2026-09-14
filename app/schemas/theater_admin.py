from pydantic import BaseModel,EmailStr
from uuid import UUID

#theater admin
class TheaterWithAdminCreate(BaseModel):
    city_id: UUID
    theater_id: UUID
    admin_username: EmailStr
    admin_password: str