from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TheatreCreate(BaseModel):
    city_id : UUID
    theater_name : str
    address : str
    status: str = "active"


class TheatreUpdate(BaseModel):
    theater_name : str | None = None
    address : str |  None = None
    status: str | None = None


class TheatreDetails(BaseModel):
    theater_id : UUID
    city_id : UUID
    theater_name : str
    address : str
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)