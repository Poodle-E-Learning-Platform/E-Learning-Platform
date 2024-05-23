from fastapi import APIRouter, Header
from common.authentication import get_user_or_raise_401
from services import users_service
from services.tag_services import create_tag # delete_tag
from common.responses import CreatedSuccessfully, Forbidden, BadRequest, NotFound
from data.models import Tag, CreateTagRequest


tags_router = APIRouter(prefix="/tags")


@tags_router.post("/", response_model=Tag)
async def create_new_tag(request: CreateTagRequest, token: str = Header(...)):
    user = get_user_or_raise_401(token)

    if not users_service.is_teacher(user.user_id):
        return Forbidden()

    tag = create_tag(request.tag_name)
    if isinstance(tag, BadRequest):
        return BadRequest()

    return tag


# @tags_router.delete("/{tag_id}")
# async def remove_tag(tag_id: int, token: str = Header(...)):
#     user = get_user_or_raise_401(token)
#
#     if not users_service.is_teacher(user.user_id):
#         return Forbidden()
#
#     result = delete_tag(tag_id)
#     if isinstance(result, NotFound):
#         return NotFound()
#
#     return result
