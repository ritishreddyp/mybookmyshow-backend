from sqlalchemy import Column, Integer, String,DateTime,Date,Boolean
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship
from app.models.languages import SQlanguages

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQmovies(Base):

    __tablename__ = "Movies"
    movie_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    poster_url = Column(String, nullable=False)
    status = Column(String, default="inactive", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    languages = relationship("SQlanguages",secondary="movie_languages",back_populates="movies")
    shows = relationship("SQshows", back_populates="movie")
    