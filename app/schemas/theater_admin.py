from pydantic import BaseModel
from uuid import UUID

#theater admin
class TheaterAdminCreate(BaseModel):
    theater_id: UUID
    admin_password: str