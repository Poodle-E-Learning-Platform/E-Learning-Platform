from fastapi import APIRouter, Header
from data.models import LoginInformation, TeacherRegistration, StudentRegistration
from common.responses import BadRequest, Unauthorized, NotFound
from services import users_service
from common.constants import USER_LOGGED_OUT_RESPONSE

users_router = APIRouter(prefix="/users")


@users_router.post("/login")
def user_login(data: LoginInformation):
    user = users_service.try_login(data.email, data.password)
    if user:
        token = users_service.create_jwt_token(user.user_id, user.email)
        return {"token": token}
    return BadRequest("Incorrect e-mail or password!")


@users_router.post("/logout")
def user_logout(token: str = Header()):
    if not users_service.is_authenticated(token):
        return Unauthorized(content="Invalid token!")

    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User already logged out!")

    users_service.add_token_to_blacklist(token)
    return {"message": "User successfully logged out!"}


@users_router.get("/info")
def user_info(token: str = Header()):
    payload = users_service.verify_jwt_token(token)
    if payload:
        user = users_service.get_by_id(payload["user_id"])
        if user:
            return {"id": user.user_id, "email": user.email}
    return Unauthorized(content="Invalid token!")


@users_router.post("/register/teachers")
def register_teacher(data: TeacherRegistration):
    user = users_service.create_teacher(data)
    return user if user else BadRequest(f'E-mail "{data.email}" is already in use!')


@users_router.post("/register/students")
def register_student(data: StudentRegistration):
    user = users_service.create_student(data)
    return user if user else BadRequest(content=f'E-mail "{data.email}" is already in use!')


@users_router.get("/teachers/info")
def get_teacher_info(token: str = Header()):
    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    user = users_service.from_token(token)
    if user:
        teacher = users_service.get_teacher_by_user_id(user.user_id)
        if teacher:
            return teacher

    return NotFound(content="Teacher not found!")


@users_router.put("/teachers/info")
def update_teacher_info(data: dict, token: str = Header()):
    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    user = users_service.from_token(token)
    if user:
        updated_teacher = users_service.update_teacher_info(user.user_id, data)
        if updated_teacher:
            return updated_teacher

    return BadRequest(content="Failed to update teacher information!")


@users_router.put("/student/info")
def update_teacher_info(data: dict, token: str = Header()):
    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    user = users_service.from_token(token)
    if user:
        updated_student = users_service.update_student_info(user.user_id, data)
        if updated_student:
            return updated_student

    return BadRequest(content="Failed to update teacher information!")



