from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Table,Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base


movie_languages = Table("movie_languages",Base.metadata,
                        
    Column("movie_id", Integer, ForeignKey("Movies.movie_id", ondelete="CASCADE"), primary_key=True),
    Column("language_id", Integer, ForeignKey("Languages.language_id", ondelete="CASCADE"), primary_key=True))


class SQlanguages(Base):
    __tablename__ = "Languages"

    language_id = Column(Integer, primary_key=True, autoincrement=True)
    language_name = Column(String, nullable=False)
    status = Column(String, default="available", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    movies = relationship("SQmovies", secondary=movie_languages, back_populates="languages")
    shows = relationship("SQshows", back_populates="language")

