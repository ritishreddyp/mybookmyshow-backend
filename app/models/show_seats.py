from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Float
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship

class SQshow_seats(Base):

    __tablename__ = "ShowSeats"
    show_seat_id = Column(Integer, primary_key=True, autoincrement=True)
    show_id = Column(Integer, ForeignKey("Shows.show_id", ondelete="CASCADE"), nullable=False)
    seat_id = Column(Integer, ForeignKey("Seats.id", ondelete="CASCADE"), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, default= "available" ,nullable=False)
    lock_expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    show = relationship("SQshows", back_populates="show_seats")
    seat = relationship("SQseats", back_populates="show_seats")
    booking_items = relationship("SQbooking_items", back_populates="show_seat")
    