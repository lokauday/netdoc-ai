# ================================================================
# NetDoc AI — FastAPI Backend (Root Application)
# Python 3.13.9 compatible
# ================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routers import ai, audit, topology, inventory, snmp, backup, auth


# ------------------------------------------------
# APP INIT
# ------------------------------------------------
app = FastAPI(
    title="NetDoc AI Backend",
    version="1.0.0",
    description="Backend APIs for AI processing, topology, auditing, SNMP monitoring, automation, and inventory."
)


# ------------------------------------------------
# CORS — Allow Streamlit Frontend
# ------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # You can restrict later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------
# ROUTERS
# ------------------------------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Services"])
app.include_router(audit.router, prefix="/api/audit", tags=["Security Audit"])
app.include_router(topology.router, prefix="/api/topology", tags=["Topology Generator"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Device Inventory"])
app.include_router(snmp.router, prefix="/api/snmp", tags=["SNMP Monitoring"])
app.include_router(backup.router, prefix="/api/backup", tags=["Config Backup"])


# ------------------------------------------------
# ROOT TEST ENDPOINT
# ------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "Running",
        "app": "NetDoc AI Backend",
        "version": "1.0.0",
        "message": "Backend API is operational."
    }
