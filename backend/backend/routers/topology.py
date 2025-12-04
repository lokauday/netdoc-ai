# ====================================================================
# NetDoc AI — Topology Router API
# ====================================================================

from fastapi import APIRouter
from pydantic import BaseModel

from services.topology_engine import generate_topology

router = APIRouter()


class ConfigBody(BaseModel):
    config: str


@router.post("/")
def topology(data: ConfigBody):
    topo = generate_topology(data.config)
    return {"topology": topo}
