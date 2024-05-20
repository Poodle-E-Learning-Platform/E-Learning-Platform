from mariadb import IntegrityError
from data.database import insert_query
from data.models import Section, CreateSection
from common.responses import NotFound
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


# def update_section(section_id: int, section: CreateSection) -> bool:
#     sql = "UPDATE sections SET title=?, content=?, description=?, external_resource=? WHERE section_id=?"
#     params = (section.title, section.content, section.description, section.external_resource, section_id)
#     return update_query(sql, params)
#
# def delete_section(section_id: int) -> bool:
#     sql = "DELETE FROM sections WHERE section_id=?"
#     return update_query(sql, (section_id,))
#
# def get_section_by_id(section_id: int) -> Optional[Section]:
#     sql = "SELECT section_id, title, content, description, external_resource, course_id FROM sections WHERE section_id=?"
#     result = read_query(sql, (section_id,))
#     if result:
#         section_data = result[0]
#         return Section(**section_data)
#     return None