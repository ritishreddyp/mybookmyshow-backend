from pydantic import BaseModel 


class theaters(BaseModel):
    theatre_id: int 
    theatre_name: str
    address: str
    city_id: int
    contact_number: str