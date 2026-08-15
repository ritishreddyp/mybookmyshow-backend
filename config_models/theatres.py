from sqlalchemy import Column, Integer, String,DateTime,ForeignKey
from datetime import datetime
from config import Base

class SQtheaters(Base):

    __tablename__ = "Theatres"
    theater_id = Column(Integer,primary_key=True,autoincrement=True)
    movie_id = Column(Integer,ForeignKey("Movies.moive_id"),nullable=False)
    city_id = Column(Integer,ForeignKey("City.city_id"),nullable=False)
    theater_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    contact_number = Column(String, unique=True, nullable=False)
    status =  Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)