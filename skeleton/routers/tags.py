from fastapi import APIRouter, Header
from common.authentication import get_user_or_raise_401
from services import users_service
from services.tag_services import create_tag, delete_tag, add_tag_to_course, remove_tag_from_course, \
    get_course_with_tags
from common.responses import CreatedSuccessfully, Forbidden, BadRequest, NotFound
from data.models import Tag, CreateTagRequest


tags_router = APIRouter(prefix="/tags")


@tags_router.post("/", response_model=Tag)
async def create_new_tag(request: CreateTagRequest, token: str = Header(...)):
    """
        Create a new tag.

        Parameters:
        - request: CreateTagRequest
            The request body containing the tag name to be created.
        - token: str
            The authentication token provided in the header.

        Returns:
        - Tag: The created tag object if successful.
        - Forbidden: If the user is not a teacher.
        - BadRequest: If the tag creation fails.

        """
    user = get_user_or_raise_401(token)

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="Only teachers can create new tags!")

    tag = create_tag(request.tag_name)
    if isinstance(tag, BadRequest):
        return BadRequest(content="Can not create this tag!")

    return tag


@tags_router.delete("/{tag_id}")
async def remove_tag(tag_id: int, token: str = Header(...)):
    """
        Remove an existing tag.

        Parameters:
        - tag_id: int
            The ID of the tag to be removed.
        - token: str
            The authentication token provided in the header.

        Returns:
        - Message: Tag deleted successfully.
        - NotFound: If the tag is not found.
        - Forbidden: If the user is not a teacher.

        """
    user = get_user_or_raise_401(token)

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="Only teachers can delete tags!")

    result = delete_tag(tag_id)
    if isinstance(result, NotFound):
        return NotFound(content="Tag not found!")

    return result


@tags_router.post("/{tag_id}/courses/{course_id}")
async def add_tag_to_course_endpoint(tag_id: int, course_id: int, token: str = Header(...)):
    """
        Add a tag to a course.

        Parameters:
        - tag_id: int
            The ID of the tag to be added.
        - course_id: int
            The ID of the course to which the tag will be added.
        - token: str
            The authentication token provided in the header.

        Returns:
        - Message: Tag added to course successfully.
        - NotFound: If the course or tag is not found.
        - Forbidden: If the user is not a teacher.
        - BadRequest: If the operation fails.

        """
    user = get_user_or_raise_401(token)

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="Only teachers can add tags to courses!")

    result = add_tag_to_course(course_id, tag_id)
    if isinstance(result, NotFound):
        return NotFound(content="Course or tag not found!")
    if isinstance(result, BadRequest):
        return BadRequest(content="Can not add tag to course!")

    return result


@tags_router.delete("/{tag_id}/courses/{course_id}")
async def remove_tag_from_course_endpoint(tag_id: int, course_id: int, token: str = Header(...)):
    """
        Remove a tag from a course.

        Parameters:
        - tag_id: int
            The ID of the tag to be removed.
        - course_id: int
            The ID of the course from which the tag will be removed.
        - token: str
            The authentication token provided in the header.

        Returns:
        - Message: Tag removed from course successfully.
        - NotFound: If the course or tag is not found.
        - Forbidden: If the user is not a teacher.

        """
    user = get_user_or_raise_401(token)

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="Only teachers can remove tags from courses!")

    result = remove_tag_from_course(course_id, tag_id)
    if isinstance(result, NotFound):
        return NotFound(content="Course or tag not found!")

    return result


@tags_router.get("/courses/{course_id}")
async def get_course_with_tags_endpoint(course_id: int):
    """
        Get a course with its associated tags.

        Parameters:
        - course_id: int
            The ID of the course.

        Returns:
        - NotFound: If the course is not found.
        - Dictionary: The course with its tags.

        """
    result = get_course_with_tags(course_id)
    if isinstance(result, NotFound):
        return NotFound(content="Course not found!")

    return result
