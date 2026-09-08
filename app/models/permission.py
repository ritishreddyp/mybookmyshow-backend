import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base


class SQPermission(Base):
    __tablename__ = "Permissions"

    permission_id = Column(String , primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String , unique=True, nullable=False) 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    roles = relationship("SQRole", secondary="RolePermissions", back_populates="permissions")