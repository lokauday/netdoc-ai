# ====================================================================
# NetDoc AI — Auth Utilities (JWT Decoding)
# ====================================================================

from fastapi import Header, HTTPException
from services.auth_engine import verify_jwt


def get_current_user(token: str = Header(...)):
    """
    Extract current authenticated user from JWT token.
    token is expected in 'token' header
    """
    payload = verify_jwt(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload
