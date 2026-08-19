from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class SQlanguages(Base):
    __tablename__ = "languages"

    language_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("Movies.movie_id"), nullable=False)
    language_name = Column(String, nullable=False)
    status = Column(String, default="available", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    movie = relationship("SQmovies", back_populates="languages")
    shows = relationship("SQshows", back_populates="language")