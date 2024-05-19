from data.database import insert_query, read_query
from data.models import Course, CreateCourse, CourseWithSections
from mariadb import IntegrityError
from services import users_service
from common.responses import NotFound


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
