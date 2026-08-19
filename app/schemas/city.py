from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CityCreate(BaseModel):
    city_name : str
    state : str


class CityUpdate(BaseModel):
    city_name : str | None = None
    state : str | None = None


class CityDetails(BaseModel):
    city_id : int
    city_name : str
    state : str
    created_at : datetime
    updated_at : datetime
    model_config = ConfigDict(from_attributes=True)