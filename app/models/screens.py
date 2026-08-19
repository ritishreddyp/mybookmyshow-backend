from sqlalchemy import Column, Integer, String,DateTime,ForeignKey
from datetime import datetime
from src.app.core.config import Base
from sqlalchemy.orm import relationship

class SQscreens(Base):

    __tablename__ = "Screens"
    screen_id = Column(Integer,primary_key=True,autoincrement=True)
    theater_id = Column(Integer,ForeignKey("Theatres.theater_id"),nullable=False)
    screen_name = Column(String, nullable=False)
    screen_type = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)
    status = Column(String, default="inactive", nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    theater = relationship("SQtheaters", back_populates="screens")
    seats = relationship("SQseats", back_populates="screen", cascade="all, delete-orphan")
    shows = relationship("SQshows", back_populates="screen")