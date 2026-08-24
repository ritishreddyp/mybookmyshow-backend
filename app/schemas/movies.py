from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.languages import LanguageDetails

class MovieCreate(BaseModel):
    title : str
    description : str
    genre : str
    duration_minutes : int
    release_date : date
    poster_url : str
    status: str = "active"


class MovieUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    genre: str | None = None
    duration_minutes: int | None = None
    release_date: date | None = None
    poster_url: str | None = None
    status: str | None = None


class MovieDetails(BaseModel):
    movie_id : int
    title : str
    description : str
    genre : str
    duration_minutes : int
    release_date : date
    poster_url : str
    status : str
    created_at: datetime
    updated_at: datetime
    languages: list[LanguageDetails] = []
    model_config = ConfigDict(from_attributes=True)

