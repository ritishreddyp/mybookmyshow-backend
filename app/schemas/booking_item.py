from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookingItemCreate(BaseModel):
    booking_id : int
    show_seat_id : int
    price : float
 

class BookingItemDetails(BaseModel):

    booking_item_id : int
    booking_id : int
    show_seat_id : int
    price :  float
    created_at : datetime
    updated_at : datetime
    model_config = ConfigDict(from_attributes=True)