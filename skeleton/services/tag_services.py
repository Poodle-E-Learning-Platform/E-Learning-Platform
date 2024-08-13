from data.database import insert_query, read_query, delete_query
from data.models import Tag
from mariadb import IntegrityError
from common.responses import NotFound, BadRequest


def create_tag(tag_name: str) -> Tag | BadRequest:
    try:
        tag_id = insert_query(
            """insert into course_tags (tag_name) values (?)""",
            (tag_name,)
        )
        if tag_id:
            return Tag(tag_id=tag_id, tag_name=tag_name)
        return BadRequest(content="Tag creation failed")
    except IntegrityError:
        return BadRequest(content="Tag with this name already exists")


def delete_tag(tag_id: int) -> dict | NotFound:
    tag_data = read_query(
        """SELECT * FROM course_tags WHERE tag_id = ?""",
        (tag_id,)
    )
    if not tag_data:
        return NotFound(content=f"Tag with ID {tag_id} not found")

    delete_query(
        """DELETE FROM course_tags WHERE tag_id = ?""",
        (tag_id,)
    )
    return {"message": "Tag deleted successfully"}


def add_tag_to_course(course_id: int, tag_id: int) -> dict | NotFound | BadRequest:
    course_query = "SELECT * FROM courses WHERE course_id = ?"
    course_data = read_query(course_query, (course_id,))
    if not course_data:
        return NotFound(content=f"Course with ID {course_id} not found!")

    tag_query = "SELECT * FROM course_tags WHERE tag_id = ?"
    tag_data = read_query(tag_query, (tag_id,))
    if not tag_data:
        return NotFound(content=f"Tag with ID {tag_id} not found!")

    mapping_query = "SELECT * FROM course_tag_mapping WHERE course_id = ? AND tag_id = ?"
    mapping_data = read_query(mapping_query, (course_id, tag_id))
    if mapping_data:
        return BadRequest(content=f"Tag with ID {tag_id} is already associated with course ID {course_id}")

    insert_query(
        "INSERT INTO course_tag_mapping (course_id, tag_id) VALUES (?, ?)",
        (course_id, tag_id)
    )

    return {"message": "Tag added to course successfully"}


def remove_tag_from_course(course_id: int, tag_id: int) -> dict | NotFound:
    mapping_query = "SELECT * FROM course_tag_mapping WHERE course_id = ? AND tag_id = ?"
    mapping_data = read_query(mapping_query, (course_id, tag_id))
    if not mapping_data:
        return NotFound(content=f"Tag with ID {tag_id} is not associated with course ID {course_id}")

    delete_query(
        "DELETE FROM course_tag_mapping WHERE course_id = ? AND tag_id = ?",
        (course_id, tag_id)
    )

    return {"message": "Tag removed from course successfully"}


def get_course_with_tags(course_id: int) -> dict | NotFound:
    course_query = """
    SELECT title
    FROM courses
    WHERE course_id = ?
    """
    course_data = read_query(course_query, (course_id,))
    if not course_data:
        return NotFound(content=f"Course with ID {course_id} not found!")

    tags_query = """
    SELECT ct.tag_id, ct.tag_name
    FROM course_tag_mapping ctm
    JOIN course_tags ct ON ctm.tag_id = ct.tag_id
    WHERE ctm.course_id = ?
    """
    tags_data = read_query(tags_query, (course_id,))

    course_with_tags = {
        "course_id": course_id,
        "course_name": course_data[0][0],
        "tags": tags_data
    }

    return course_with_tags


def get_all_courses_with_tags() -> list:
    courses_query = """
    SELECT course_id, title
    FROM courses
    """
    courses_data = read_query(courses_query)

    courses_with_tags = []

    for course in courses_data:
        course_id = course[0]
        course_name = course[1]

        tags_query = """
        SELECT ct.tag_id, ct.tag_name
        FROM course_tag_mapping ctm
        JOIN course_tags ct ON ctm.tag_id = ct.tag_id
        WHERE ctm.course_id = ?
        """
        tags_data = read_query(tags_query, (course_id,))

        course_with_tags = {
            "course_id": course_id,
            "course_name": course_name,
            "tags": tags_data
        }

        courses_with_tags.append(course_with_tags)

    return courses_with_tags

