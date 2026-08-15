from sqlalchemy import Column, Integer, String,DateTime ,Float,ForeignKey
from datetime import datetime
from config import Base


class SQbooking_section(Base):

    __tablename__ = "BookingSection"
    booking_id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.user_id"),nullable=False)
    show_id = Column(Integer,ForeignKey("Shows.show_id"),nullable=False)
    total_amount = Column(Float, nullable=False)
    booking_status = Column(String, default= "Pending", nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)