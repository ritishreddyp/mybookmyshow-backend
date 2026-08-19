from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Float
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship

class SQbooking_items(Base):

    __tablename__ = "BookingItems"
    booking_item_id = Column(Integer,primary_key=True,autoincrement=True)
    booking_id = Column(Integer,ForeignKey("BookingSection.booking_id"),nullable=False)
    show_seat_id = Column(Integer,ForeignKey("ShowSeats.show_seat_id"),nullable=False)
    price = Column(Float,nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    booking = relationship("SQbooking_section", back_populates="booking_items")
    show_seat = relationship("SQshow_seats", back_populates="booking_items")