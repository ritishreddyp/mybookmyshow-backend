from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.db import Base

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQbooking_items(Base):
    __tablename__ = "BookingItems"

    booking_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("BookingSection.booking_id"), nullable=False)
    show_seat_id = Column(UUID(as_uuid=True), ForeignKey("ShowSeats.show_seat_id"), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    booking = relationship("SQbooking_section", back_populates="booking_items")
    show_seat = relationship("SQshow_seats", back_populates="booking_items")