from sqlalchemy import Column, Integer, String,DateTime,ForeignKey,Float
from datetime import datetime
from config import Base


class SQshow_seats(Base):

    __tablename__ = "ShowSeats"
    show_seat_id = Column(Integer,primary_key=True,autoincrement=True)
    show_id = Column(Integer,ForeignKey("Shows.shoe_id"),nullable=False)
    seat_id = Column(Integer,ForeignKey("Seats.seat_id"),nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, default= "available" ,nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    