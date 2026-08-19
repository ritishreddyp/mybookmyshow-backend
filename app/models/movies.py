from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Date
from datetime import datetime
from src.app.core.config import Base
from sqlalchemy.orm import relationship

class SQmovies(Base):

    __tablename__ = "Movies"
    movie_id = Column(Integer,primary_key=True,autoincrement=True)
    
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    poster_url = Column(String, nullable=False)
    status = Column(String, default="inactive", nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    languages = relationship("SQlanguages", back_populates="movie", cascade="all, delete-orphan")
    shows = relationship("SQshows", back_populates="movie")
    