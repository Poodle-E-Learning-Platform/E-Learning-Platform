from fastapi import APIRouter, Header, HTTPException
from data.models import Course, CreateCourse, CourseWithSections, UpdateCourse
from common.responses import BadRequest, Unauthorized, Forbidden, NotFound
from services import courses_service, users_service
from common.authentication import get_user_or_raise_401


courses_router = APIRouter(prefix="/courses")


@courses_router.get("/teachers")
def get_all_teacher_courses(token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User is logged out! Login required to perform this task!")

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="User must be a teacher in order to view all courses!")

    teacher = users_service.get_teacher_by_user_id(user.user_id)

    courses = courses_service.get_all_teacher_courses(user.user_id)
    if not courses:
        return NotFound(content=f"Teacher with id:{teacher.teacher_id} has not created any courses yet")

    return courses


@courses_router.get("/students")
def get_all_student_courses(token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User is logged out! Login required to perform this task!")

    student = users_service.get_student_by_user_id(user.user_id)

    if not student:
        return Forbidden(content="User must be a student to access enrolled courses!")

    courses = courses_service.get_all_student_courses(student.student_id)

    if not courses:
        return NotFound(content="No courses found for the student.")

    return courses


@courses_router.get("/{course_id}/teachers")
def get_teacher_course_by_id(course_id: int, order: str = "asc", title: str = None, token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User is logged out! Login required to perform this task!")

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="User must be a teacher in order to view all courses!")

    teacher = users_service.get_teacher_by_user_id(user.user_id)

    course = courses_service.get_teacher_course_by_id(user.user_id, course_id, order, title)

    if not course:
        return NotFound(content=f"Course with id {course_id} not found!")

    if teacher.teacher_id != course.owner_id:
        return Forbidden(content=f"Teacher must be owner of course with id: {course.course_id} in order to view it!")

    return course


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


@courses_router.put("/{course_id}")
def update_course_details(course_id: int, data: UpdateCourse, token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return Unauthorized(content="User is logged out! Login required to perform this task!")

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="User is not authorized! Only teachers that are owners "
                                 "can update a course!")

    updated_course = courses_service.update_course(course_id, data, user.user_id)

    if not updated_course:
        return NotFound(content=f"Course with id: {course_id} not found")

    updated_course.is_premium = bool(updated_course.is_premium)

    return updated_course

# {
#     "title":"English for Beginners",
#     "description":"Introductory course into the world of English!",
#     "objectives":"Give new students a grasp of the basics.",
#     "owner_id":1
# }
