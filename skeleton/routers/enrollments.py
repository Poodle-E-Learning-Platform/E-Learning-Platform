from fastapi import APIRouter, Header
from common.responses import BadRequest, Forbidden, NotFound, Conflict
from services import users_service, enrollments_service, courses_service
from common.authentication import get_user_or_raise_401
from common.constants import PREMIUM_COURSE_LIMIT, USER_LOGGED_OUT_RESPONSE

enrollments_router = APIRouter(prefix="/enrollments")


@enrollments_router.get("/reports/students", tags=["Enrollments"])
def get_teacher_students_report(token: str = Header()):
    """
        Generate a report for a teacher about his students.

        Parameters:
        - token: str
            The authentication token provided in the header.

        Returns:
        - List of students: The students enrolled in the teacher's courses.
        - Forbidden: If the user is not a teacher.
        - NotFound: If no students are found for the given teacher's courses.
        - Unauthorized: If the token is blacklisted.
        """
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


@enrollments_router.post("/courses/{course_id}/subscribe", tags=["Enrollments"])
def subscribe_to_course(course_id: int, token: str = Header()):
    """
        Subscribe a student to a course.

        Parameters:
        - course_id: int
            The ID of the course to subscribe to.
        - token: str
            The authentication token provided in the header.

        Returns:
        - Message: A message indicating successful subscription.
        - Forbidden: If the user is not a student.
        - NotFound: If the course is not found.
        - Conflict: If the student is already subscribed to the course or exceeds the premium course limit.
        - Unauthorized: If the token is blacklisted.
        """
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


@enrollments_router.post("/courses/{course_id}/unsubscribe", tags=["Enrollments"])
def unsubscribe_from_course(course_id: int, token: str = Header()):
    """
        Unsubscribe a student from a course.

        Parameters:
        - course_id: int
            The ID of the course to unsubscribe from.
        - token: str
            The authentication token provided in the header.

        Returns:
        - Message: A message indicating successful withdrawal from the course.
        - Forbidden: If the user is not a student.
        - NotFound: If the course is not found.
        - Conflict: If the student is already not subscribed to the course.
        - Unauthorized: If the token is blacklisted.
        """
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
