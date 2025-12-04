# ====================================================================
# NetDoc AI — Authentication Engine (JWT + Hashing)
# ====================================================================

import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.models import User, APIKey, Workspace

JWT_SECRET = os.getenv("JWT_SECRET", "NETDOC_SECRET_123")
JWT_ALGO = "HS256"
JWT_EXP_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------------
# PASSWORD HASHING
# ---------------------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


# ---------------------------------------------------------------
# JWT TOKENS
# ---------------------------------------------------------------
def create_jwt(user: User) -> str:
    payload = {
        "sub": user.email,
        "user_id": user.id,
        "role": user.role,
        "workspace_id": user.workspace_id,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXP_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def verify_jwt(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except Exception:
        return None


# ---------------------------------------------------------------
# API KEYS
# ---------------------------------------------------------------
def create_api_key(db: Session, user: User, label: str = "default") -> APIKey:
    key = os.urandom(16).hex()

    api_key = APIKey(
        key=key,
        label=label,
        user_id=user.id
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key


# ---------------------------------------------------------------
# CREATE USER
# ---------------------------------------------------------------
def create_user(db: Session, email: str, password: str, full_name: str = None) -> User:
    workspace = Workspace(name=f"{email}'s Workspace")
    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        workspace_id=workspace.id,
        role="admin" if email.endswith("@admin.com") else "user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------------------------------------------------------------
# AUTHENTICATE USER
# ---------------------------------------------------------------
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
