from datetime import datetime
from pydantic import BaseModel, ConfigDict,Field
from uuid import UUID

class LanguageCreate(BaseModel):
    language_name : str


class LanguageUpdate(BaseModel):
    language_name: str | None = None
    status: str | None = None


class LanguageDetails(BaseModel):
    language_id : UUID
    language_name : str
    status : str
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)


class MovieLanguageAssignment(BaseModel):
    language_ids: list[UUID] = Field(..., min_length=1)