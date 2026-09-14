from sqlalchemy import Column, Integer, String,DateTime,Float,ForeignKey
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQpayments(Base):

    __tablename__ = "Payments"
    payment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("BookingSection.booking_id"), nullable=False)
    transaction_id = Column(String, unique=True, nullable=False)
    payment_method = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    payment_status = Column(String, default="Processing", nullable=False)

    payment_date = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at =  Column(DateTime, default=datetime.now, nullable=False)

    booking_section = relationship("SQbooking_section", back_populates="payments")