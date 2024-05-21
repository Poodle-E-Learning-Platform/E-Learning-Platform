from data.database import read_query, insert_query, delete_query
from services import courses_service
from common.responses import NotFound, Conflict
from data.models import StudentReport


def is_student_enrolled(student_id: int, course_id: int) -> bool:
    enrollment_check_query = """select count(*) from enrollments where students_student_id = ? 
    and courses_course_id = ?"""
    result = read_query(enrollment_check_query, (student_id, course_id))
    return result[0][0] > 0


def is_student_not_enrolled(student_id: int, course_id: int) -> bool:
    not_enrolled_check_query = """select count(*) from enrollments where students_student_id = ? 
                                  and courses_course_id = ?"""
    result = read_query(not_enrolled_check_query, (student_id, course_id))
    return result[0][0] == 0


def get_premium_course_count(student_id: int) -> int:
    premium_count_query = """select count(*) from enrollments join courses on 
    enrollments.courses_course_id = courses.course_id where 
    enrollments.students_student_id = ? and courses.is_premium = 1"""
    premium_count_data = read_query(premium_count_query, (student_id,))
    return premium_count_data[0][0]


def subscribe_to_course(student_id: int, course_id: int) -> dict | NotFound | Conflict:
    course = courses_service.get_course_by_id_simpler(course_id)

    if not course:
        return NotFound(content="Course not found!")

    is_premium = course.is_premium

    if is_student_enrolled(student_id, course_id):
        return Conflict(content="Student is already subscribed to this course!")

    if is_premium:
        premium_count = get_premium_course_count(student_id)
        if premium_count >= 5:
            return Conflict(content="Student cannot subscribe to more than 5 premium courses at a time!")

    subscribe_query = """insert into enrollments (students_student_id, courses_course_id) values (?, ?)"""

    insert_query(subscribe_query, (student_id, course_id))

    return {"message": f"Student with id:{student_id} successfully subscribed course with id:{course.course_id}."}


def unsubscribe_from_course(student_id: int, course_id: int) -> dict | NotFound | Conflict:
    course = courses_service.get_course_by_id_simpler(course_id)
    if not course:
        return NotFound(content=f"Course with ID {course_id} not found!")

    # Check if the student is enrolled in the course
    if not is_student_enrolled(student_id, course_id):
        return Conflict(content="Student is not subscribed to this course.")

    unsubscribe_query = "delete from enrollments where students_student_id = ? and courses_course_id = ?"
    delete_query(unsubscribe_query, (student_id, course_id))

    return {"message": f"Student with id:{student_id} successfully unsubscribed from course with id:{course_id}."}


def get_students_by_teacher_id(teacher_id: int) -> list[StudentReport]:
    query = """
    SELECT s.student_id, s.first_name, s.last_name, s.email, c.course_id, c.title
    FROM students s
    JOIN enrollments e ON s.student_id = e.students_student_id
    JOIN courses c ON e.courses_course_id = c.course_id
    WHERE c.owner_id = ?
    """
    data = read_query(query, (teacher_id,))

    return [StudentReport.from_query_result(*row) for row in data]