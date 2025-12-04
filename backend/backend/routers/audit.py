# ====================================================================
# NetDoc AI — Audit Router API
# ====================================================================

from fastapi import APIRouter
from pydantic import BaseModel
from services.audit_engine import run_security_audit

router = APIRouter()


class ConfigBody(BaseModel):
    config: str


@router.post("/")
def audit_config(data: ConfigBody):
    result = run_security_audit(data.config)
    return {"audit": result}
