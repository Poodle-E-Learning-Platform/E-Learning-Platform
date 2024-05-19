from data.database import insert_query, read_query
from data.models import Course, CreateCourse, CourseWithSections, Section
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

        sections = [Section.from_query_result(*row) for row in section_data]

        course_with_sections = CourseWithSections(
            course_id=course_row[0],
            title=course_row[1],
            description=course_row[2],
            objectives=course_row[3],
            sections=sections
        )

        courses_with_sections.append(course_with_sections)

    return courses_with_sections


def create_course(user_id: int, data: CreateCourse) -> Course | None | NotFound:
    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return NotFound(content="Teacher not found!")

    owner_id = teacher.teacher_id

    try:
        course_id = insert_query(
            """insert into courses (title, description, objectives, owner_id) values (?, ?, ?, ?)""",
            (data.title, data.description, data.objectives, owner_id)
        )
        if course_id:
            return Course(course_id=course_id, title=data.title, description=data.description,
                          objectives=data.objectives, owner_id=owner_id)
        return None
    except IntegrityError:
        return None
