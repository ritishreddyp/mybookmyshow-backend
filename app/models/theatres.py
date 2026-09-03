from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Boolean
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship
class SQtheaters(Base):

    __tablename__ = "Theaters"
    theater_id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("City.city_id"), nullable=False)
    theater_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    status =  Column(String, default="active", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    city = relationship("SQcity", back_populates="theaters")
    screens = relationship("SQscreens", back_populates="theater", cascade="all, delete-orphan")