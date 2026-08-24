from datetime import datetime
from pydantic import BaseModel, ConfigDict,Field


class LanguageCreate(BaseModel):
    language_name : str

class LanguageUpdate(BaseModel):
    language_name: str | None = None
    status: str | None = None
    
class LanguageDetails(BaseModel):
    language_id : int
    movie_id : int
    language_name : str
    status : str
    created_at : datetime
    updated_at : datetime
    model_config = ConfigDict(from_attributes=True)


