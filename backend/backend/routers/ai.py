# ====================================================================
# NetDoc AI — AI API Router
# ====================================================================

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.ai_engine import (
    ai_troubleshoot,
    ai_design,
    ai_log_analyzer,
    ai_generate_commands,
    ai_document_config,
)

router = APIRouter()


# Shared request body
class TextBody(BaseModel):
    text: str


# -------------------------
# TROUBLESHOOTING
# -------------------------
@router.post("/troubleshoot")
def troubleshoot(data: TextBody):
    result = ai_troubleshoot(data.text)
    return {"result": result}


# -------------------------
# DESIGN ENGINE
# -------------------------
@router.post("/design")
def design(data: TextBody):
    result = ai_design(data.text)
    return {"result": result}


# -------------------------
# LOG ANALYZER
# -------------------------
@router.post("/logs")
def analyze_logs(data: TextBody):
    result = ai_log_analyzer(data.text)
    return {"result": result}


# -------------------------
# COMMAND GENERATOR
# -------------------------
@router.post("/commands")
def command_gen(data: TextBody):
    result = ai_generate_commands(data.text)
    return {"result": result}


# -------------------------
# DOCUMENTATION GENERATOR
# -------------------------
@router.post("/documentation")
def documentation(data: TextBody):
    result = ai_document_config(data.text)
    return {"result": result}
