# ====================================================================
# NetDoc AI — Backup Router API
# ====================================================================

from fastapi import APIRouter
from pydantic import BaseModel

from services.backup_engine import get_running_config

router = APIRouter()


class BackupRequest(BaseModel):
    ip: str
    username: str
    password: str


@router.post("/")
def backup_config(req: BackupRequest):
    config = get_running_config(req.ip, req.username, req.password)
    return {"config": config}
