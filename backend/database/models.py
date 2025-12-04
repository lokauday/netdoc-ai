# ====================================================================
# NetDoc AI — SQLAlchemy Models (Users, Workspaces, API Keys, Logs)
# ====================================================================

from sqlalchemy import (
    Column, Integer, String, Boolean,
    ForeignKey, DateTime, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base


# ---------------------------------------------------------------
# WORKSPACE MODEL (multi-tenant support)
# ---------------------------------------------------------------
class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="workspace")


# ---------------------------------------------------------------
# USER MODEL
# ---------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String, nullable=True)

    role = Column(String, default="user")  # admin/user/viewer

    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)
    workspace = relationship("Workspace", back_populates="users")

    api_keys = relationship("APIKey", back_populates="user")
    logs = relationship("ActivityLog", back_populates="user")

    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


# ---------------------------------------------------------------
# API KEY MODEL (for programmatic access)
# ---------------------------------------------------------------
class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    label = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="api_keys")


# ---------------------------------------------------------------
# ACTIVITY LOG (tracking events)
# ---------------------------------------------------------------
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="logs")
