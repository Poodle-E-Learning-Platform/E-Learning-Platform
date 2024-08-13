from data.database import insert_query, read_query, delete_query, update_query
from data.models import Section, CreateSection, UpdateSection
from services import users_service, courses_service


def create_new_section(data: CreateSection) -> Section | None:
    section_id = insert_query(
        """insert into sections (title, content, description, external_resource, course_id)
             values (?, ?, ?, ?, ?)""",
        (data.title, data.content, data.description, data.external_resource, data.course_id))

    if section_id:
        return Section(section_id=section_id, title=data.title, content=data.content,
                       description=data.description, external_resource=data.external_resource,
                       course_id=data.course_id)
    return None


def update_section(section_id: int, data: UpdateSection) -> bool:
    rows_affected = update_query(
        """update sections set title = ?, content = ?, description = ?, external_resource = ? 
           where section_id = ?""",
        (data.title, data.content, data.description, data.external_resource, section_id)
    )

    if rows_affected:
        return True

    return False


def delete_section(section_id: int) -> bool:
    rows_affected = delete_query(
        """delete from sections where section_id = ?""",
        (section_id,)
    )
    if rows_affected:
        return True

    return False


def get_course_id_for_section(section_id: int) -> int | None:
    section_query = """select course_id from sections where section_id = ?"""
    section_data = read_query(section_query, (section_id,))

    if section_data:
        return section_data[0][0]

    return None


def is_section_owner(section_id: int, user_id: int) -> bool:
    course_id = get_course_id_for_section(section_id)
    if not course_id:
        return False

    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return False

    course = courses_service.get_teacher_course_by_id(user_id, course_id)
    if not course:
        return False

    return course.owner_id == teacher.teacher_id
