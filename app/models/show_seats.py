from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Float,Boolean
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQshow_seats(Base):

    __tablename__ = "ShowSeats"
    show_seat_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    show_id = Column(UUID(as_uuid=True), ForeignKey("Shows.show_id", ondelete="CASCADE"), nullable=False)
    seat_id = Column(UUID(as_uuid=True), ForeignKey("Seats.seat_id", ondelete="CASCADE"), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, default= "available" ,nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    lock_expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    show = relationship("SQshows", back_populates="show_seats")
    seat = relationship("SQseats", back_populates="show_seats")
    booking_items = relationship("SQbooking_items", back_populates="show_seat")
    