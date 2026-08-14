from pydantic import BaseModel 

class booking_items(BaseModel):
    booking_item_id: int
    booking_id: int
    show_seat_id: int
    event_session_id: int
    match_id: int
    quantity: int
    price: float