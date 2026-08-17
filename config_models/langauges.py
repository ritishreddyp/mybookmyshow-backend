from sqlalchemy import Column, Integer, String,DateTime,ForeignKey
from datetime import datetime
from config import Base
from sqlalchemy.orm import relationship

class SQlanguages(Base):

    __tablename__ = "languages"
    language_id = Column(Integer,primary_key=True,autoincrement=True)
    movie_id = Column(Integer,ForeignKey("Movies.movie_id"),nullable=False)
    language_name = Column(String, nullable=False)
    status = Column(String, default="avaliable", nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    movie = relationship("SQmovies", back_populates="languages")
    shows = relationship("SQshows", back_populates="language")