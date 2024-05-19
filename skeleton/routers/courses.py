from fastapi import APIRouter, Header
from data.models import Course, CreateCourse, CourseWithSections
from common.responses import BadRequest, Unauthorized, Forbidden, NotFound
from services import courses_service, users_service
from common.authentication import get_user_or_raise_401


courses_router = APIRouter(prefix="/courses")


@courses_router.get("/")
def get_all_courses(token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User is logged out! Login required to perform this task!")

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="User must be a teacher in order to view all courses!")

    teacher = users_service.get_teacher_by_user_id(user.user_id)

    courses = courses_service.get_all_courses(user.user_id)
    if not courses:
        return NotFound(content=f"Teacher with id:{teacher.teacher_id} has not created any courses yet")

    return courses


@courses_router.post("/")
async def create_course(data: CreateCourse, token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User is logged out! Login required to perform this task!")

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="User is not authorized to create a course!")

    course = courses_service.create_course(user.user_id,data)
    if not course:
        return BadRequest(content="Course with this title already exists or other error occurred")

    return course

# {
#     "title":"English for Beginners",
#     "description":"Introductory course into the world of English!",
#     "objectives":"Give new students a grasp of the basics.",
#     "owner_id":1
# }
