from sqlalchemy import Column, Integer, String,DateTime
from datetime import datetime
from src.app.core.config import Base
from sqlalchemy.orm import relationship

class SQcity(Base):

    __tablename__ = "City"
    city_id = Column(Integer,primary_key=True,autoincrement=True)
    city_name = Column(String,nullable=False)
    state = Column(String,nullable=False)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    theaters = relationship("SQtheaters", back_populates="city", cascade="all, delete-orphan")