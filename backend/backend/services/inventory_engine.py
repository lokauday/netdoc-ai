# ====================================================================
# NetDoc AI — Inventory Engine (CRUD + Multi-Tenant)
# ====================================================================

from sqlalchemy.orm import Session
from database.models import User
from database.models import Workspace
from typing import List, Dict
from database.models import APIKey
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


# -------------------------------
# INVENTORY MODEL (Dynamic)
# -------------------------------

from database.session import Base
from sqlalchemy.orm import relationship


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    hostname = Column(String)
    ip_address = Column(String)
    vendor = Column(String)
    model = Column(String)
    location = Column(String)

    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    workspace = relationship("Workspace")


def init_inventory_table(engine):
    Base.metadata.create_all(bind=engine)


# -------------------------------
# CRUD FUNCTIONS
# -------------------------------
def add_device(db: Session, workspace_id: int, data: Dict):
    device = Device(
        hostname=data["hostname"],
        ip_address=data["ip_address"],
        vendor=data["vendor"],
        model=data["model"],
        location=data["location"],
        workspace_id=workspace_id
    )

    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def get_all_devices(db: Session, workspace_id: int):
    return db.query(Device).filter(Device.workspace_id == workspace_id).all()


def delete_device(db: Session, device_id: int, workspace_id: int):
    device = (
        db.query(Device)
        .filter(Device.id == device_id, Device.workspace_id == workspace_id)
        .first()
    )
    if not device:
        return False

    db.delete(device)
    db.commit()
    return True
