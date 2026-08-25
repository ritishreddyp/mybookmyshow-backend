from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ScreenCreate(BaseModel):
    theater_id : int
    screen_name : str
    screen_type : str 
    status : str = "active"


class ScreenUpdate(BaseModel):
    screen_name : str | None = None
    screen_type : str | None = None
    status : str      | None = None


class ScreenDetails(BaseModel):
    screen_id : int
    theater_id : int
    screen_name : str
    screen_type : str
    status : str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)