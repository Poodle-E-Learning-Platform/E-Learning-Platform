from fastapi import HTTPException, APIRouter, Depends, Header
from data.models import LoginInformation, RegistrationInformation
from common.responses import BadRequest
from services import users_service

users_router = APIRouter(prefix="/users")


@users_router.post("/login")
async def user_login(data: LoginInformation):
    user = users_service.try_login(data.username, data.password)
    if user:
        token = users_service.create_jwt_token(user.id, user.username)
        return {"token": token}
    return BadRequest("Login information not valid!")


@users_router.get("/info")
async def user_info(token: str = Header()):
    payload = users_service.verify_jwt_token(token)
    if payload:
        user = users_service.get_by_id(payload["user_id"])
        if user:
            return {"id": user.id, "username": user.username, "is_admin": user.is_admin}
    raise HTTPException(status_code=401, detail="Invalid token")


@users_router.post("/register")
async def register_user(data: RegistrationInformation):
    user = users_service.create(data.username, data.password, data.email, data.name)
    return user if user else BadRequest(f'Username "{data.username}" is already taken!')
