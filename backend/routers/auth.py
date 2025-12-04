# ====================================================================
# NetDoc AI — Authentication Router (JWT Login + Signup)
# ====================================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.session import get_db
from services.auth_engine import (
    create_user, authenticate_user, create_jwt
)


router = APIRouter()


# ---------------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------------
class SignupModel(BaseModel):
    email: str
    password: str
    full_name: str | None = None


class LoginModel(BaseModel):
    email: str
    password: str


# ---------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------
@router.post("/signup")
def signup(data: SignupModel, db: Session = Depends(get_db)):
    user = create_user(db, data.email, data.password, data.full_name)
    return {"message": "User created", "email": user.email}


@router.post("/login")
def login(data: LoginModel, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt(user)
    return {"token": token, "email": user.email, "role": user.role}
