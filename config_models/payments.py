from sqlalchemy import Column, Integer, String, Float,ForeignKey,DateTime
from config import Base

class payments(Base):

    __tablename__ = "Payments"
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer,ForeignKey(""),nullable=False)
    amount = Column(Float,nullable=False)
    payment_method = Column(String,nullable=False)
    payment_status = Column(,nullable=False)
    transaction_id = Column(Float,nullable=False)
    payment_time: datetime