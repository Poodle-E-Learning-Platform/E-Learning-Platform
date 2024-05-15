from fastapi import HTTPException
from data.models import User
from services.users_service import verify_jwt_token, get_by_id


def get_user_or_raise_401(token: str):
    payload = verify_jwt_token(token)
    if payload:
        user = get_by_id(payload["user_id"])
        if user:
            return user
    raise HTTPException(status_code=401, detail="Invalid token")
