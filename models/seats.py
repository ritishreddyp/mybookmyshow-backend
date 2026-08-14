from pydantic import BaseModel 

class seats(BaseModel):
    seat_id: int
    screen_id: int
    row_name: str
    seat_number: int
    seat_type: str