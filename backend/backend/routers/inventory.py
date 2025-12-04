# ====================================================================
# NetDoc AI — Inventory API Router
# ====================================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from utils.auth_utils import get_current_user
from services.inventory_engine import (
    add_device,
    get_all_devices,
    delete_device,
)
from services.activity_engine import log_action
from database.session import get_db

router = APIRouter()


# --------------------------
# REQUEST MODELS
# --------------------------
class DeviceModel(BaseModel):
    hostname: str
    ip_address: str
    vendor: str
    model: str
    location: str


class DeleteModel(BaseModel):
    id: int


# --------------------------
# ROUTES
# --------------------------
@router.post("/add")
def add_new_device(
    data: DeviceModel,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    device = add_device(db, user["workspace_id"], data.dict())

    log_action(
        db,
        user_id=user["user_id"],
        action="Add Device",
        details=f"Added {data.hostname}"
    )

    return {"added": device.id}


@router.get("/list")
def list_devices(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    devices = get_all_devices(db, user["workspace_id"])
    return {"devices": [vars(d) for d in devices]}


@router.delete("/delete")
def delete_device_route(
    req: DeleteModel,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    ok = delete_device(db, req.id, user["workspace_id"])

    if not ok:
        raise HTTPException(status_code=404, detail="Device not found")

    log_action(
        db,
        user_id=user["user_id"],
        action="Delete Device",
        details=f"Deleted device {req.id}"
    )

    return {"deleted": True}
