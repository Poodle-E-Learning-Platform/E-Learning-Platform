from fastapi import APIRouter, Header, HTTPException
from data.models import Section, CreateSection
from common.responses import BadRequest, Unauthorized, Forbidden, NotFound
from services import courses_service, users_service, sections_service
from common.authentication import get_user_or_raise_401


sections_router = APIRouter(prefix="/sections")


@sections_router.post("/")
def create_new_section(data: CreateSection, token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User is logged out! Login required to perform this task!")

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="User must be a teacher in order to create a section within a course!")

    teacher = users_service.get_teacher_by_user_id(user.user_id)

    course = courses_service.get_course_by_id(user.user_id, data.course_id)

    if teacher.teacher_id != course.owner_id:
        return Forbidden(content=f"Teacher must be owner of course with id:{course.course_id} "
                                 f"in order to create a new section!")

    section = sections_service.create_new_section(user.user_id, data)

    if section:
        return section
    else:
        return BadRequest(content="Failed to create section!")

