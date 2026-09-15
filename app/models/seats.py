from sqlalchemy import Column, Integer, String,DateTime,ForeignKey
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQseats(Base):

    __tablename__ = "Seats"
    seat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    theater_id = Column(UUID(as_uuid=True), ForeignKey("Theaters.theater_id", ondelete="CASCADE"), nullable=False)
    screen_id = Column(UUID(as_uuid=True), ForeignKey("Screens.screen_id", ondelete="CASCADE"), nullable=False)
    seat_row = Column(String, nullable=False)
    seat_number = Column(String, nullable=False) 
    seat_type = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    screen = relationship("SQscreens", back_populates="seats")
    show_seats = relationship("SQshow_seats", back_populates="seat")