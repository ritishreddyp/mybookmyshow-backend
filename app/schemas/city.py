from pydantic import BaseModel 
from datetime import datetime

class City(BaseModel):
    
    city_name: str
    state: str
    
 