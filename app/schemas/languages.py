from pydantic import BaseModel
from datetime import datetime

class languages(BaseModel):
    language_id: int
    movie_id: int
    language_name: str
    status: str
    created_at: datetime
    updated_at: datetime 
    