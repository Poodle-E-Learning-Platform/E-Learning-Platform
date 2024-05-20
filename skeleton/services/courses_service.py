from data.database import insert_query, read_query, update_query
from data.models import Course, CreateCourse, CourseWithSections, Section, UpdateCourse
from mariadb import IntegrityError
from services import users_service
from common.responses import NotFound


def get_all_courses(user_id: int) -> list[CourseWithSections] | NotFound | None:
    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return NotFound(content="Teacher not found!")

    owner_id = teacher.teacher_id

    course_query = """select * from courses where owner_id = ?"""
    course_params = (owner_id,)
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


def get_course_by_id(user_id: int, course_id: int, order: str = "asc", title: str = None) -> CourseWithSections | NotFound:
    teacher = users_service.get_teacher_by_user_id(user_id)

    if not teacher:
        return NotFound(content="Teacher not found!")

    owner_id = teacher.teacher_id

    course_query = """SELECT * FROM courses WHERE owner_id = ? AND course_id = ?"""
    course_params = (owner_id, course_id)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return NotFound(content=f"Course with ID {course_id} not found!")

    course_row = course_data[0]
    sections = []

    section_query = """SELECT * FROM sections WHERE course_id = ?"""

    if title:
        section_query += """ AND title LIKE ?"""
        section_params = (course_id, f"%{title}%")
    else:
        section_params = (course_id,)

    section_query += """ ORDER BY section_id"""
    if order.lower() == "desc":
        section_query += """ DESC"""

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


def get_course_by_id_simpler(course_id) -> Course | NotFound:
    course_query = """select * from courses where course_id = ?"""
    course_params = (course_id,)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return NotFound(content=f"Course with ID {course_id} not found!")

    course_row = course_data[0]

    return Course(course_id=course_row[0],
                  title=course_row[1],
                  description=course_row[2],
                  objectives=course_row[3],
                  owner_id=course_row[-3],
                  is_premium=bool(course_row[-2]),
                  rating=course_row[-1]
                  )



def create_course(user_id: int, data: CreateCourse) -> Course | None | NotFound:
    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return NotFound(content="Teacher not found!")

    owner_id = teacher.teacher_id

    try:
        course_id = insert_query(
            """insert into courses (title, description, objectives, owner_id, is_premium) values (?, ?, ?, ?, ?)""",
            (data.title, data.description, data.objectives, owner_id, data.is_premium)
        )
        if course_id:
            return Course(course_id=course_id, title=data.title, description=data.description,
                          objectives=data.objectives, owner_id=owner_id, is_premium=data.is_premium)
        return None
    except IntegrityError:
        return None


def update_course(course_id: int, data: UpdateCourse, user_id: int) -> Course | NotFound | None:
    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return NotFound(content="Teacher not found!")

    course = get_course_by_id(teacher.users_user_id, course_id)

    if not course:
        return NotFound(content=f"Course with ID {course_id} not found.")

    try:
        update_query(
            """UPDATE courses SET title = ?, description = ?, objectives = ?, is_premium = ?
             WHERE course_id = ? AND owner_id = ?""",
            (data.title, data.description, data.objectives, data.is_premium, course_id, teacher.teacher_id)
        )

        updated_course = get_course_by_id(user_id, course_id)
        return updated_course
    except IntegrityError:
        return None
