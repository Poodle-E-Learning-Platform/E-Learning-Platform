from fastapi import APIRouter, Header
from data.models import CreateCourse, UpdateCourse
from common.responses import BadRequest, Unauthorized, Forbidden, NotFound, Conflict
from services import courses_service, users_service
from common.authentication import get_user_or_raise_401
from common.constants import USER_LOGGED_OUT_RESPONSE
from services.tag_services import get_all_courses_with_tags


courses_router = APIRouter(prefix="/courses")


@courses_router.get("/teachers", tags=["Courses"])
def get_all_teacher_courses(token: str = Header()):
    """
        Retrieve all courses created by the logged-in teacher.

        Parameters:
        - token: str
            The JWT token provided in the header.

        Returns:
        - List: A list of courses created by the teacher.
        - Unauthorized: If the token is blacklisted.
        - Forbidden: If the user is not a teacher.
        - NotFound: If the teacher has not created any courses.
    """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    teacher = users_service.get_teacher_by_user_id(user.user_id)
    if not teacher:
        return Forbidden(content="User must be a teacher in order to view all courses!")

    courses = courses_service.get_all_teacher_courses(teacher.teacher_id)
    if not courses:
        return NotFound(content=f"Teacher with id:{teacher.teacher_id} has not created any courses yet")

    return courses


@courses_router.get("/students", tags=["Courses"])
def get_all_student_courses(token: str = Header()):
    """
        Retrieve all courses the logged-in student is enrolled in.

        Parameters:
        - token: str
            The JWT token provided in the header.

        Returns:
        - List: A list of courses the student is enrolled in.
        - Unauthorized: If the token is blacklisted.
        - Forbidden: If the user is not a student.
        - NotFound: If the student is not enrolled in any courses.
        """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    student = users_service.get_student_by_user_id(user.user_id)
    if not student:
        return Forbidden(content="User must be a student to access enrolled courses!")

    courses = courses_service.get_all_student_courses(student.student_id)
    if not courses:
        return NotFound(content="Student is not enrolled in any courses yet!")

    return courses


@courses_router.get("/{course_id}/teachers", tags=["Courses"])
def get_teacher_course_by_id(course_id: int, order: str = "asc", title: str = None, token: str = Header()):
    """
        Retrieve a specific course created by the logged-in teacher.

        Parameters:
        - course_id: int
            The ID of the course to retrieve.
        - order: str, optional
            The order in which to retrieve the sections in the course (default is "asc").
        - title: str, optional
            The title filter for the sections in the course (default is None).
        - token: str
            The JWT token provided in the header.

        Returns:
        - Course: The course with the specified ID.
        - Unauthorized: If the token is blacklisted.
        - Forbidden: If the user is not a teacher or not the owner of the course.
        - NotFound: If the course is not found.
    """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    teacher = users_service.get_teacher_by_user_id(user.user_id)
    if not teacher:
        return Forbidden(content="User must be a teacher in order to view all courses!")

    course = courses_service.get_teacher_course_by_id(teacher.teacher_id, course_id, order, title)
    if not course:
        return NotFound(content=f"Course with id {course_id} not found!")

    if teacher.teacher_id != course.owner_id:
        return Forbidden(content=f"Teacher must be owner of course with id: {course.course_id} in order to view it!")

    return course


@courses_router.get("/{course_id}/students", tags=["Courses"])
def get_student_course_by_id(course_id: int, order: str = "asc", title: str = None, token: str = Header()):
    """
        Retrieve a specific course the logged-in student is enrolled in.

        Parameters:
        - course_id: int
            The ID of the course to retrieve.
        - order: str, optional
            The order in which to retrieve the sections in the course (default is "asc").
        - title: str, optional
            The title filter for the sections in the course (default is None).
        - token: str
            The JWT token provided in the header.

        Returns:
        - Course: The course with the specified ID.
        - Unauthorized: If the token is blacklisted.
        - Forbidden: If the user is not a student.
        - NotFound: If the course is not found.
        """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    student = users_service.get_student_by_user_id(user.user_id)
    if not student:
        return Forbidden(content="User must be a student in order to view a specific course with its sections!")

    course = courses_service.get_student_course_by_id(student.student_id, course_id, order, title)
    if not course:
        return NotFound(f"Course with id:{course_id} not found!")

    is_enrolled = courses_service.is_student_enrolled_in_course(student.student_id, course.course_id)

    if not is_enrolled and course.is_premium:
        return Forbidden(content="Access denied. This is a premium course and the student is not enrolled.")

    return course


@courses_router.post("/", tags=["Courses"])
def create_course(data: CreateCourse, token: str = Header()):
    """
        Create a new course.

        Parameters:
        - data: CreateCourse
            The data for the new course.
        - token: str
            The JWT token provided in the header.

        Returns:
        - Course: The created course.
        - Unauthorized: If the token is blacklisted.
        - Forbidden: If the user is not a teacher.
        - BadRequest: If the course title already exists or other error occurs.
    """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    teacher = users_service.get_teacher_by_user_id(user.user_id)
    if not teacher:
        return Forbidden(content="User is not authorized to create a course!")

    course = courses_service.create_course(teacher.teacher_id, data)
    if not course:
        return BadRequest(content="Course with this title already exists or other error occurred")

    return course


@courses_router.put("/{course_id}", tags=["Courses"])
def update_course_details(course_id: int, data: UpdateCourse, token: str = Header()):
    """
        Update the details of an existing course.

        Parameters:
        - course_id: int
            The ID of the course to update.
        - data: UpdateCourse
            The new data for the course.
        - token: str
            The JWT token provided in the header.

        Returns:
        - Course: The updated course.
        - Unauthorized: If the token is blacklisted.
        - Forbidden: If the user is not the owner of the course.
        - NotFound: If the course is not found.
    """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    teacher = users_service.get_teacher_by_user_id(user.user_id)
    if not teacher:
        return Forbidden(content="User is not authorized! Only teachers that are owners "
                                 "can update a course!")

    course = courses_service.get_teacher_course_by_id(teacher.teacher_id, course_id)
    if not course:
        return NotFound(content=f"Course with ID {course_id} not found.")

    updated_course = courses_service.update_course(course_id, data, user.user_id)

    if not updated_course:
        return NotFound(content=f"Course with id: {course_id} not found")

    updated_course.is_premium = bool(updated_course.is_premium)

    return updated_course


@courses_router.delete("/{course_id}", tags=["Courses"])
def delete_course(course_id: int, token: str = Header()):
    """
        Delete an existing course.

        Parameters:
        - course_id: int
            The ID of the course to delete.
        - token: str
            The JWT token provided in the header.

        Returns:
        - dict: A message indicating the course was successfully deleted.
        - Unauthorized: If the user is not a teacher or if the token is blacklisted.
        - NotFound: If the course is not found.
        - Conflict: If the course is already deleted.
        - BadRequest: If the user is not the owner of the course or if deletion fails.
    """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    teacher = users_service.get_teacher_by_user_id(user.user_id)
    if not teacher:
        return Unauthorized(content="User must be a teacher to delete a course!")

    course = courses_service.get_course_by_id_simpler(course_id)
    if not course:
        return NotFound(content=f"Course with id:{course_id} not found!")

    if courses_service.is_course_deleted(course_id):
        return Conflict(content=f"Course with id:{course_id} has already been deleted!")

    if teacher.teacher_id != course.owner_id:
        return BadRequest(content=f"Teacher must be owner of course with id:{course_id} in order to delete it!")

    course_has_enrolled_students = courses_service.course_has_enrolled_students(course_id)

    if course_has_enrolled_students:
        return Forbidden(content=f"Cannot delete course with ID {course_id} because students are enrolled in it!")

    deleted_course = courses_service.delete_course_if_no_enrollments(course_id)

    if not deleted_course:
        BadRequest(content=f"Failed to delete course with id:{course_id}")

    return {"message": "Course deleted successfully"}


@courses_router.get("/tags", tags=["Courses"])
def get_all_courses_with_associated_tags():
    """
        Retrieve all courses along with their associated tags.

        Returns:
        - List: A list of courses along with their tags.
    """
    result = get_all_courses_with_tags()
    return result

