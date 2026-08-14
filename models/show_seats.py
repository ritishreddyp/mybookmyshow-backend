from pydantic import BaseModel 


class show_seats(BaseModel):
    show_seat_id: int
    show_id: int
    seat_id: int
    price: float
    status: str