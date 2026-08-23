from sqlalchemy import Column, Integer, String,DateTime
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship

class SQUser(Base):

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(String, default= "active" , nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    bookings = relationship("SQbooking_section", back_populates="user")