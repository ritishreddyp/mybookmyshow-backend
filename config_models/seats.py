from sqlalchemy import Column, Integer, String,DateTime,ForeignKey
from datetime import datetime
from config import Base
from sqlalchemy.orm import relationship

class SQseats(Base):

    __tablename__ = "Seats"
    seat_id = Column(Integer,primary_key=True,autoincrement=True)
    screen_id = Column(Integer,ForeignKey("Screens.screen_id"),nullable=False)
    seat_number = Column(String, nullable=False)
    seat_row = Column(String, nullable=False)
    seat_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    screen = relationship("SQscreens", back_populates="seats")
    show_seats = relationship("SQshow_seats", back_populates="seat")