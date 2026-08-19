from sqlalchemy import Column, Integer, String,DateTime,ForeignKey
from datetime import datetime
from src.app.core.config import Base
from sqlalchemy.orm import relationship

class SQtickets(Base):

    __tablename__ = "Tickets"
    ticket_id = Column(Integer,primary_key=True,autoincrement=True)
    booking_id = Column(Integer,ForeignKey("BookingSection.booking_id"),nullable=False)
    show_id = Column(Integer,ForeignKey("Shows.show_id"),nullable=False)
    ticket_code = Column(String, unique=True , nullable=False)
    ticket_status = Column(String,default= "Pending", nullable=False)
    issued_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    booking = relationship("SQbooking_section", back_populates="tickets")
    show = relationship("SQshows", back_populates="tickets")