from pydantic import BaseModel 


class screens(BaseModel):
    screen_id: int
    theatre_id: int
    screen_name: str
    total_seats: int