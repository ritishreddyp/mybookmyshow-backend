from sqlalchemy import Column, Integer, String,DateTime,Float,ForeignKey
from datetime import datetime
from config import Base
from sqlalchemy.orm import relationship

class SQpayments(Base):

    __tablename__ = "Payments"
    payment_id = Column(Integer,primary_key=True,autoincrement=True)
    booking_id = Column(Integer,ForeignKey("BookingSection.booking_id"),nullable=False)
    transaction_id = Column(String, unique=True, nullable=False)
    payment_method = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    payment_status = Column(String, default="Processing", nullable=False)
    payment_date = Column(DateTime, onupdate=datetime.now, nullable=False)
    created_at =  Column(DateTime, default=datetime.now, nullable=False)

    booking = relationship("SQbooking_section", back_populates="payments")