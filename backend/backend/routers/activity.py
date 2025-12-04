# ====================================================================
# NetDoc AI — Activity Log Router
# ====================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.auth_utils import get_current_user
from database.models import ActivityLog
from database.session import get_db

router = APIRouter()


@router.get("/")
def activity_list(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    logs = (
        db.query(ActivityLog)
        .filter(ActivityLog.user_id == user["user_id"])
        .order_by(ActivityLog.timestamp.desc())
        .limit(50)
        .all()
    )

    return {"logs": [vars(l) for l in logs]}
