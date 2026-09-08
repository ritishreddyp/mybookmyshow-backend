import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.db import Base


role_permissions = Table(
    "RolePermissions",
    Base.metadata,
    Column("role_id", String(36), ForeignKey("Roles.role_id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", String(36), ForeignKey("Permissions.permission_id", ondelete="CASCADE"), primary_key=True)
)


class SQPermission(Base):
    __tablename__ = "Permissions"

    permission_id = Column(String , primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String , unique=True, nullable=False) 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    roles = relationship("SQRole", secondary=role_permissions, back_populates="permissions")

class SQRole(Base):
    __tablename__ = "Roles"

    role_id = Column(String , primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String , unique=True, nullable=False) 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    permissions = relationship("SQPermission", secondary=role_permissions, back_populates="roles")
    users = relationship("SQUser", back_populates="role")