from pydantic import BaseModel 
from datetime import date

class movies(BaseModel):
    movie_id: int
    title: str
    description: str
    genre: str
    duration_minutes: int
    release_date: date
    poster_url: str
    status: str
    