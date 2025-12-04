# ====================================================================
# NetDoc AI — SNMP Router API
# ====================================================================

from fastapi import APIRouter
from pydantic import BaseModel

from services.snmp_engine import poll_device

router = APIRouter()


class SNMPRequest(BaseModel):
    ip: str
    community: str


@router.post("/")
def snmp_poll(req: SNMPRequest):
    data = poll_device(req.ip, req.community)
    return {"device": data}
