from fastapi import APIRouter, Header
from data.models import LoginInformation, TeacherRegistration, StudentRegistration
from common.responses import BadRequest, Unauthorized, NotFound
from services import users_service

users_router = APIRouter(prefix="/users")


@users_router.post("/login")
async def user_login(data: LoginInformation):
    user = users_service.try_login(data.email, data.password)
    if user:
        token = users_service.create_jwt_token(user.user_id, user.email)
        return {"token": token}
    return BadRequest("Incorrect e-mail or password!")


@users_router.post("/logout")
async def user_logout(token: str = Header()):
    if not users_service.is_authenticated(token):
        return Unauthorized(content="Invalid token!")

    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User already logged out!")

    users_service.add_token_to_blacklist(token)
    return {"message": "User successfully logged out!"}


@users_router.get("/info")
async def user_info(token: str = Header()):
    payload = users_service.verify_jwt_token(token)
    if payload:
        user = users_service.get_by_id(payload["user_id"])
        if user:
            return {"id": user.user_id, "email": user.email}
    return Unauthorized(content="Invalid token!")


@users_router.post("/register/teacher")
async def register_teacher(data: TeacherRegistration):
    user = users_service.create_teacher(data)
    return user if user else BadRequest(f'E-mail "{data.email}" is already in use!')


@users_router.post("/register/student")
async def register_student(data: StudentRegistration):
    user = users_service.create_student(data)
    return user if user else BadRequest(content=f'E-mail "{data.email}" is already in use!')


@users_router.get("/teacher/info")
async def get_teacher_info(token: str = Header()):
    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User is logged out! Login required to perform this task!")

    user = users_service.from_token(token)
    if user:
        teacher = users_service.get_teacher_by_user_id(user.user_id)
        if teacher:
            return teacher

    return NotFound(content="Teacher not found!")


@users_router.put("/teacher/info")
async def update_teacher_info(data: dict, token: str = Header()):
    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User is logged out! Login required to perform this task!")

    user = users_service.from_token(token)
    if user:
        updated_teacher = users_service.update_teacher_info(user.user_id, data)
        if updated_teacher:
            return updated_teacher

    return BadRequest(content="Failed to update teacher information!")


