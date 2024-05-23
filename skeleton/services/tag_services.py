from data.database import insert_query, read_query, delete_query
from data.models import Tag
from mariadb import IntegrityError
from common.responses import NotFound, BadRequest


def create_tag(tag_name: str) -> Tag | BadRequest:
    try:
        tag_id = insert_query(
            """INSERT INTO course_tags (tag_name) VALUES (?)""",
            (tag_name,)
        )
        if tag_id:
            return Tag(tag_id=tag_id, tag_name=tag_name)
        return BadRequest(content="Tag creation failed")
    except IntegrityError:
        return BadRequest(content="Tag with this name already exists")


# def delete_tag(tag_id: int) -> dict | NotFound:
#     tag_data = read_query(
#         """SELECT * FROM course_tags WHERE tag_id = ?""",
#         (tag_id,)
#     )
#     if not tag_data:
#         return NotFound(content=f"Tag with ID {tag_id} not found")
#
#     delete_query(
#         """DELETE FROM course_tags WHERE tag_id = ?""",
#         (tag_id,)
#     )
#     return {"message": "Tag deleted successfully"}
