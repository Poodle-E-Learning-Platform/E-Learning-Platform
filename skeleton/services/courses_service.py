from data.database import insert_query, read_query
from data.models import Course, CreateCourse, CourseWithSections
from mariadb import IntegrityError


def create_course(data: CreateCourse) -> Course | None:
    try:
        course_id = insert_query(
            """INSERT INTO courses (title, description, objectives, owner_id) VALUES (?, ?, ?, ?)""",
            (data.title, data.description, data.objectives, data.owner_id)
        )
        if course_id:
            return Course(course_id=course_id, title=data.title, description=data.description,
                          objectives=data.objectives, owner_id=data.owner_id)
        return None
    except IntegrityError:
        return None
