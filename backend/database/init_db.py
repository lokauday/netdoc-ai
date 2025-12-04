# ====================================================================
# NetDoc AI — Initialize Database
# ====================================================================

from .session import Base, engine
from .models import User, Workspace, APIKey, ActivityLog


def init_db():
    Base.metadata.create_all(bind=engine)
