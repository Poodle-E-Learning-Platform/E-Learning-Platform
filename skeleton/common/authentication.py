from fastapi import HTTPException
from data.models import User
from services.users_service import is_authenticated, from_token


def get_user_or_raise_401(token: str):
    if not is_authenticated(token):
        raise HTTPException(status_code=401)
    return from_token(token)
