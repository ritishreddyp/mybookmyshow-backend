from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.db import Base

import uuid
from sqlalchemy.dialects.postgresql import UUID

class SQMainAdmin(Base):
    __tablename__ = "main_admins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())