from sqlalchemy import Column, Integer, String,DateTime,Boolean
from datetime import datetime
from app.core.db import Base
from sqlalchemy.orm import relationship

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQcity(Base):

    __tablename__ = "City"
    city_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    city_name = Column(String,nullable=False)
    state = Column(String,nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    theaters = relationship("SQtheaters", back_populates="city", cascade="all, delete-orphan")