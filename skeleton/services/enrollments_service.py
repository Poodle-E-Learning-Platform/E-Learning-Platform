from data.database import read_query, insert_query, delete_query
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


def subscribe_to_course(student_id: int, course_id: int):
    subscribe_query = """insert into enrollments (students_student_id, courses_course_id) values (?, ?)"""
    insert_query(subscribe_query, (student_id, course_id))


def unsubscribe_from_course(student_id: int, course_id: int):
    unsubscribe_query = "delete from enrollments where students_student_id = ? and courses_course_id = ?"
    delete_query(unsubscribe_query, (student_id, course_id))


def get_students_by_teacher_id(teacher_id: int) -> list[StudentReport]:
    query = """
    select s.student_id, s.first_name, s.last_name, s.email, c.course_id, c.title
    from students s
    join enrollments e ON s.student_id = e.students_student_id
    join courses c on e.courses_course_id = c.course_id
    where c.owner_id = ?
    """
    data = read_query(query, (teacher_id,))

    return [StudentReport.from_query_result(*row) for row in data]
