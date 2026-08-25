from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict


class ShowCreate(BaseModel):
    theater_id: int
    screen_id : int
    movie_id : int
    language_id : int
    show_date : date
    show_time : time
    base_price : float
    status : str = "active"


class ShowUpdate(BaseModel):
    show_date : date | None = None
    show_time : time | None = None
    base_price : float | None = None
    status: str | None = None


class ShowDetails(BaseModel):
    show_id : int
    screen_id : int
    movie_id : int
    language_id : int
    show_date : date
    show_time : time
    base_price : float
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)