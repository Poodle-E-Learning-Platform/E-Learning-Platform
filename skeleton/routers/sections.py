from fastapi import APIRouter, Header, HTTPException
from data.models import Section, CreateSection, UpdateSection
from common.responses import BadRequest, Unauthorized, Forbidden, NotFound
from services import courses_service, users_service, sections_service
from common.authentication import get_user_or_raise_401
from common.constants import USER_LOGGED_OUT_RESPONSE


sections_router = APIRouter(prefix="/sections")


@sections_router.post("/")
def create_new_section(data: CreateSection, token: str = Header()):
    """
        Create a new section within a course.

        Parameters:
        - data: CreateSection
            The data required to create a new section.
        - token: str
            The authentication token provided in the header.

        Returns:
        - Section: The created section object if successful.
        - Forbidden: If the user is not a teacher or does not own the course.
        - BadRequest: If section creation fails.
        - Unauthorized: If the token is blacklisted.
        """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="User must be a teacher in order to create a section within a course!")

    teacher = users_service.get_teacher_by_user_id(user.user_id)

    course = courses_service.get_teacher_course_by_id(user.user_id, data.course_id)

    if teacher.teacher_id != course.owner_id:
        return Forbidden(content=f"Teacher must be owner of course with id:{course.course_id} "
                                 f"in order to create a new section!")

    section = sections_service.create_new_section(user.user_id, data)

    if section:
        return section
    else:
        return BadRequest(content="Failed to create section!")


@sections_router.put("/{section_id}")
def update_section(section_id: int, data: UpdateSection, token: str = Header()):
    """
        Update an existing section.

        Parameters:
        - section_id: int
            The ID of the section to be updated.
        - data: UpdateSection
            The data required to update the section.
        - token: str
            The authentication token provided in the header.

        Returns:
        - Message: A message indicating success if the section is updated.
        - NotFound: If the section is not found.
        - Forbidden: If the user is not a teacher.
        - Unauthorized: If the token is blacklisted.
        """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="User must be a teacher in order to update a section!")

    updated_section = sections_service.update_section(section_id, user.user_id, data)
    if updated_section:
        return {"message": "Section updated successfully!"}
    else:
        return NotFound(content=f"Section with ID {section_id} not found!")


@sections_router.delete("/{section_id}")
def delete_section(section_id: int, token: str = Header()):
    """
        Delete an existing section.

        Parameters:
        - section_id: int
            The ID of the section to be deleted.
        - token: str
            The authentication token provided in the header.

        Returns:
        - Message: A message indicating success if the section is deleted.
        - NotFound: If the section is not found or deletion fails.
        - Forbidden: If the user is not a teacher or not the owner of the section.
        - Unauthorized: If the token is blacklisted.
        """
    user = get_user_or_raise_401(token)

    if users_service.is_token_blacklisted(token):
        return USER_LOGGED_OUT_RESPONSE

    if not users_service.is_teacher(user.user_id):
        return Forbidden(content="User must be a teacher in order to delete a section from a course!")

    if not sections_service.is_section_owner(section_id, user.user_id):
        return Forbidden(content="Teacher must be the owner of the section to delete it!")

    success = sections_service.delete_section(section_id, user.user_id)

    if success:
        return {"message": "Section deleted successfully!"}
    else:
        return NotFound(content="Section not found or failed to delete!")
