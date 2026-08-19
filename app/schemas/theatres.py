from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TheatreCreate(BaseModel):
    city_id : int
    theater_name : str
    address : str
    contact_number : str
    status: str = "active"


class TheatreUpdate(BaseModel):
    theater_name : str | None = None
    address : str |  None = None
    contact_number : str | None = None
    status: str | None = None


class TheatreDetails(BaseModel):
    theater_id : int
    city_id : int
    theater_name : str
    address : str
    contact_number : str
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)