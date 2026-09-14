from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Boolean
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQscreens(Base):

    __tablename__ = "Screens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    screen_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    theater_id = Column(UUID(as_uuid=True), ForeignKey("Theaters.theater_id"), nullable=False)
    screen_name = Column(String, nullable=False)
    screen_type = Column(String, nullable=False)
    status = Column(String, default="inactive", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    theater = relationship("SQtheaters", back_populates="screens")
    seats = relationship("SQseats", back_populates="screen", cascade="all, delete-orphan")
    shows = relationship("SQshows", back_populates="screen")