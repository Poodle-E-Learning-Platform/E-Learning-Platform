from fastapi import APIRouter, Header
from common.responses import BadRequest, Forbidden, NotFound, Conflict
from services import users_service, enrollments_service, courses_service
from common.authentication import get_user_or_raise_401
from common.constants import PREMIUM_COURSE_LIMIT, USER_LOGGED_OUT_RESPONSE

enrollments_router = APIRouter(prefix="/enrollments")


@enrollments_router.get("/reports/students")
def get_teacher_students_report(token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    teacher = users_service.get_teacher_by_user_id(user.user_id)

    if not teacher:
        return Forbidden(content="User must be a teacher to generate student reports!")

    students = enrollments_service.get_students_by_teacher_id(teacher.teacher_id)

    if not students:
        return NotFound(content="No students found for the given teacher's courses.")

    return students


@enrollments_router.post("/courses/{course_id}/subscribe")
def subscribe_to_course(course_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    student = users_service.get_student_by_user_id(user.user_id)

    if not student:
        return Forbidden(content="User must be a student to subscribe to courses!")

    course = courses_service.get_course_by_id_simpler(course_id)

    if not course:
        return NotFound(content=f"Course with id:{course_id} not found!")

    if enrollments_service.is_student_enrolled(student.student_id, course.course_id):
        return Conflict(content="Student is already subscribed to this course!")

    if course.is_premium:
        premium_count = enrollments_service.get_premium_course_count(student.student_id)
        if premium_count >= PREMIUM_COURSE_LIMIT:
            return Conflict(content="Student cannot subscribe to more than 5 premium courses at a time!")

    enrollments_service.subscribe_to_course(student.student_id, course_id)

    return {"message": f"Student with id:{student.student_id} successfully subscribed to course with id:{course_id}."}


@enrollments_router.post("/courses/{course_id}/unsubscribe")
def unsubscribe_from_course(course_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    student = users_service.get_student_by_user_id(user.user_id)

    if not student:
        return Forbidden(content="User must be a student to subscribe to courses!")

    course = courses_service.get_course_by_id_simpler(course_id)

    if not course:
        return NotFound(content=f"Course with id:{course_id} not found!")

    if enrollments_service.is_student_not_enrolled(student.student_id, course.course_id):
        return Conflict(content="Student is already not subscribed to this course!")

    enrollments_service.unsubscribe_from_course(student.student_id, course_id)

    return {"message": f"Student with id:{student.student_id} successfully unsubscribed from course with id:{course_id}."}
