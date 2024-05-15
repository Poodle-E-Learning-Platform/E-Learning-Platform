from fastapi import APIRouter, Header
from pydantic import BaseModel
from services import users_service
from data.models import User, LoginInformation
from common.responses import BadRequest
from common.authentication import get_user_or_raise_401


users_router = APIRouter(prefix="/users")


@users_router.post("/login")
async def user_login(data: LoginInformation):
    user = users_service.try_login(data.username, data.password)
    if user:
        token = users_service.create_token(user)
        return {"token": token}

    return BadRequest("Login information not valid!")


@users_router.get("/info")
async def user_info(token: str = Header()):
    user = get_user_or_raise_401(token)

    return {"id": user.id, "username": user.username, "is_admin": user.is_admin}


@users_router.post("/register")
async def register_user(data: LoginInformation):
    user = users_service.create(data.username, data.password, data.email, data.name)

    return user if user else BadRequest(f'Username "{data.username}" is already taken!')
