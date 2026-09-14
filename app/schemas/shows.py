from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class ShowCreate(BaseModel):
    theater_id: UUID
    screen_id : UUID
    movie_id : UUID
    language_id : UUID
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
    show_id : UUID
    screen_id : UUID
    movie_id : UUID
    language_id : UUID
    show_date : date
    show_time : time
    base_price : float
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)