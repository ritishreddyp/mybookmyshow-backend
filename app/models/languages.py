from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Table,UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.db import Base





movie_languages = Table("movie_languages",Base.metadata,
                        
    Column("movie_id", Integer, ForeignKey("Movies.movie_id", ondelete="CASCADE"), primary_key=True),
    Column("language_id", Integer, ForeignKey("languages.language_id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("movie_id", "language_id", name="uq_movie_language"))



class SQlanguages(Base):
    __tablename__ = "languages"

    language_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("Movies.movie_id"), nullable=False)
    language_name = Column(String, nullable=False)
    status = Column(String, default="available", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    movies = relationship("SQmovies", secondary=movie_languages, back_populates="languages")


