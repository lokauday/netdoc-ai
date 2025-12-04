# ====================================================================
# NetDoc AI — Activity Logging Engine
# ====================================================================

from sqlalchemy.orm import Session
from database.models import ActivityLog
from datetime import datetime


def log_action(db: Session, user_id: int, action: str, details: str = ""):
    entry = ActivityLog(
        user_id=user_id,
        action=action,
        details=details,
        timestamp=datetime.utcnow(),
    )
    db.add(entry)
    db.commit()
    return entry
