from services.users_service import verify_jwt_token, get_by_id, is_token_blacklisted
from common.responses import Unauthorized


def get_user_or_raise_401(token: str):
    payload = verify_jwt_token(token)
    if payload:
        user_id = payload.get("user_id")
        if is_token_blacklisted(token):
            return Unauthorized(content="User is logged out! Please log in order to perform this task!")
        user = get_by_id(user_id)
        if user:
            return user
    return Unauthorized(content="Invalid token")
