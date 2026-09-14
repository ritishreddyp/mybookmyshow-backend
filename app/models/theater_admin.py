from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.db import Base

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQTheaterAdmin(Base):
    __tablename__ = "theater_admins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, index=True)
    theater_name = Column(String, nullable=False)
    theater_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    city_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())