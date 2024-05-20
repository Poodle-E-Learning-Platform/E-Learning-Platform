from mariadb import IntegrityError
from data.database import insert_query, read_query, delete_query
from data.models import Section, CreateSection
from common.responses import NotFound, Unauthorized
from services import users_service, courses_service


def create_new_section(user_id: int, data: CreateSection) -> Section | None | NotFound:
    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return NotFound(content="Teacher not found!")

    try:
        section_id = insert_query(
            """insert into sections (title, content, description, external_resource, course_id)
             values (?, ?, ?, ?, ?)""",
            (data.title, data.content, data.description, data.external_resource, data.course_id)
        )
        if section_id:
            return Section(section_id=section_id, title=data.title, content=data.content,
                           description=data.description, external_resource=data.external_resource,
                           course_id=data.course_id)
        return None
    except IntegrityError:
        return None


def delete_section(section_id: int, user_id: int) -> bool | NotFound:
    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return NotFound(content="Teacher not found!")

    rows_affected = delete_query(
        """delete from sections where section_id = ?""",
        (section_id,)
    )
    if rows_affected:
        return True

    return False


def is_section_owner(section_id: int, user_id: int) -> bool | NotFound | Unauthorized:
    section_query = """select course_id from sections where section_id = ?"""
    section_data = read_query(section_query, (section_id,))

    if not section_data:
        return NotFound(content=f"Section with ID {section_id} not found!")

    teacher = users_service.get_teacher_by_user_id(user_id)

    if not teacher:
        return Unauthorized(content="User be a logged in teacher!")

    course_id = section_data[0][0]
    course = courses_service.get_course_by_id(user_id, course_id)

    if not course:
        return NotFound(content=f"Course with ID {course_id} not found!")

    return course.owner_id == teacher.teacher_id
