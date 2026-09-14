from sqlalchemy import Column, Integer, String,DateTime
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQUser(Base):

    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, default="public")
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(String, default= "active" , nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    bookings = relationship("SQbooking_section", back_populates="user")