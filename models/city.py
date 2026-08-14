from pydantic import BaseModel 


class Cities(BaseModel):
    cities_id: int
    city_name: str
    state: str