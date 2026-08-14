from pydantic import BaseModel 
from datetime import date, time

class shows(BaseModel):
    show_id: int
    movie_id: int
    screen_id: int
    show_date: date
    start_time: time
    end_time: time