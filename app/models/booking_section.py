from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

import uuid
from sqlalchemy.dialects.postgresql import UUID


class SQbooking_section(Base):
    __tablename__ = "BookingSection"

    booking_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    show_id = Column(UUID(as_uuid=True), ForeignKey("Shows.show_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    total_amount = Column(Float, nullable=False)
    booking_status = Column(String, default="Pending", nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    

    user = relationship("SQUser", back_populates="bookings")
    show = relationship("SQshows", back_populates="bookings")
    booking_items = relationship("SQbooking_items", back_populates="booking", cascade="all, delete-orphan")
    payments = relationship("SQpayments", back_populates="booking_section", primaryjoin="SQbooking_section.booking_id == SQpayments.booking_id")
    tickets = relationship("SQtickets", back_populates="booking", cascade="all, delete-orphan")