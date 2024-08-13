from data.database import insert_query, read_query, update_query, delete_query
from data.models import Course, CreateCourse, CourseWithSections, Section, UpdateCourse
from mariadb import IntegrityError
from services import users_service
from common.responses import NotFound, Forbidden


def get_all_teacher_courses(teacher_id: int) -> list[CourseWithSections] | None:
    course_query = """select * from courses where owner_id = ?"""
    course_params = (teacher_id,)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return None

    courses_with_sections = []

    for course_row in course_data:
        course_id = course_row[0]
        section_query = """select * from sections where course_id = ?"""
        section_params = (course_id,)
        section_data = read_query(section_query, section_params)

        if not section_data:
            sections = []
        else:
            sections = [Section.from_query_result(*row) for row in section_data]

        course_with_sections = CourseWithSections(
            course_id=course_row[0],
            title=course_row[1],
            description=course_row[2],
            objectives=course_row[3],
            owner_id=course_row[-3],
            is_premium=bool(course_row[-2]),
            sections=sections
        )

        courses_with_sections.append(course_with_sections)

    return courses_with_sections


def get_teacher_course_by_id(teacher_id: int, course_id: int, order: str = "asc", title: str = None) -> \
        CourseWithSections | None:
    course_query = """select * from courses where owner_id = ? and course_id = ?"""
    course_params = (teacher_id, course_id)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return None

    course_row = course_data[0]
    sections = []

    section_query = """select * from sections where course_id = ?"""

    if title:
        section_query += """ and title like ?"""
        section_params = (course_id, f"%{title}%")
    else:
        section_params = (course_id,)

    section_query += """ order by section_id"""
    if order.lower() == "desc":
        section_query += """ desc"""

    section_data = read_query(section_query, section_params)

    if section_data:
        sections = [Section.from_query_result(*row) for row in section_data]

    course_with_sections = CourseWithSections(
        course_id=course_row[0],
        title=course_row[1],
        description=course_row[2],
        objectives=course_row[3],
        owner_id=course_row[-3],
        is_premium=bool(course_row[-2]),
        sections=sections
    )

    return course_with_sections


def get_student_course_by_id(student_id: int, course_id: int, order: str = "asc", title: str = None) -> \
        CourseWithSections | NotFound | None:
    course_query = """select * from courses where course_id = ?"""
    course_params = (course_id,)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return None

    course_row = course_data[0]
    is_premium = bool(course_row[-2])

    if is_premium:
        enrollment_query = """select * from enrollments where courses_course_id = ? and students_student_id = ?"""
        enrollment_params = (course_id, student_id)
        enrollment_data = read_query(enrollment_query, enrollment_params)

        if not enrollment_data:
            return NotFound(content="Access denied. This is a premium course and the student is not enrolled.")

    section_query = """select * from sections where course_id = ?"""

    if title:
        section_query += """ and title like ?"""
        section_params = (course_id, f"%{title}%")
    else:
        section_params = (course_id,)

    section_query += """ order by section_id"""
    if order.lower() == "desc":
        section_query += """ desc"""

    section_data = read_query(section_query, section_params)

    sections = [Section.from_query_result(*row) for row in section_data] if section_data else []

    course_with_sections = CourseWithSections(
        course_id=course_row[0],
        title=course_row[1],
        description=course_row[2],
        objectives=course_row[3],
        owner_id=course_row[-3],
        is_premium=is_premium,
        sections=sections
    )

    return course_with_sections


def get_course_by_id_simpler(course_id) -> Course | None:
    course_query = """select * from courses where course_id = ?"""
    course_params = (course_id,)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return None

    course_row = course_data[0]

    return Course(course_id=course_row[0],
                  title=course_row[1],
                  description=course_row[2],
                  objectives=course_row[3],
                  owner_id=course_row[-3],
                  is_premium=bool(course_row[-2]),
                  rating=course_row[-1]
                  )


def get_all_student_courses(student_id: int) -> list[Course] | None:
    enrolled_query = """
    select c.course_id, c.title, c.description, c.objectives, c.owner_id, c.is_premium, c.rating
    from courses c
    join enrollments e on c.course_id = e.courses_course_id
    where e.students_student_id = ?
    """
    enrolled_params = (student_id,)
    enrolled_data = read_query(enrolled_query, enrolled_params)

    non_premium_query = """
    select c.course_id, c.title, c.description, c.objectives, c.owner_id, c.is_premium, c.rating
    from courses c
    where c.is_premium = 0
    and not exists (
        select 1
        from enrollments e
        where e.courses_course_id = c.course_id
        and e.students_student_id = ?
    )
    """
    non_premium_params = (student_id,)
    non_premium_data = read_query(non_premium_query, non_premium_params)

    courses = []

    if enrolled_data:
        courses.extend([Course.from_query_result(*row) for row in enrolled_data])

    if non_premium_data:
        courses.extend([Course.from_query_result(*row) for row in non_premium_data])

    if not courses:
        return None

    return courses


def create_course(teacher_id: int, data: CreateCourse) -> Course | None:
    owner_id = teacher_id

    course_id = insert_query(
        """insert into courses (title, description, objectives, owner_id, is_premium) values (?, ?, ?, ?, ?)""",
        (data.title, data.description, data.objectives, owner_id, data.is_premium)
    )
    if course_id:
        return Course(course_id=course_id, title=data.title, description=data.description,
                      objectives=data.objectives, owner_id=owner_id, is_premium=data.is_premium)
    return None


def update_course(course_id: int, data: UpdateCourse, teacher_id: int) -> Course | None:

    rows_affected = update_query(
            """update courses SET title = ?, description = ?, objectives = ?, is_premium = ?
             where course_id = ? and owner_id = ?""",
            (data.title, data.description, data.objectives, data.is_premium, course_id, teacher_id)
        )

    if rows_affected == 0:
        return None

    updated_course = get_teacher_course_by_id(teacher_id, course_id)

    return updated_course


def delete_course_if_no_enrollments(course_id: int) -> bool:
    delete_course_query = """delete from courses where course_id = ?"""
    delete_course_params = (course_id,)
    result = delete_query(delete_course_query, delete_course_params)

    return result > 0


def is_course_deleted(course_id: int) -> bool:
    course_query = """select * from courses where course_id = ?"""
    course_params = (course_id,)
    course_data = read_query(course_query, course_params)

    return not course_data


def is_student_enrolled_in_course(student_id: int, course_id: int) -> bool:
    enrollment_query = """select 1 from enrollments where students_student_id = ? and courses_course_id = ?"""
    enrollment_params = (student_id, course_id)
    enrollment_data = read_query(enrollment_query, enrollment_params)

    return bool(enrollment_data)


def course_has_enrolled_students(course_id: int) -> bool:
    enrollments_query = """select count(*) from enrollments where courses_course_id = ?"""
    enrollments_data = read_query(enrollments_query, (course_id,))

    if enrollments_data:
        return enrollments_data[0][0] > 0

    return False
