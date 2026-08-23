from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class SQbooking_section(Base):
    __tablename__ = "BookingSection"

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    show_id = Column(Integer, ForeignKey("Shows.show_id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    booking_status = Column(String, default="Pending", nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    user = relationship("SQUser", back_populates="bookings")
    show = relationship("SQshows", back_populates="bookings")
    booking_items = relationship("SQbooking_items", back_populates="booking", cascade="all, delete-orphan")
    payments = relationship("SQpayments", back_populates="booking", cascade="all, delete-orphan")
    tickets = relationship("SQtickets", back_populates="booking", cascade="all, delete-orphan")