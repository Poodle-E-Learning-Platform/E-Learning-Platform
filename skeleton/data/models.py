from pydantic import BaseModel, constr
from datetime import datetime, date


class Topic(BaseModel):
    id: int
    title: str = constr(pattern="^\w{1,100}$")
    category_id: int
    user_id: int
    creation_date: datetime
    best_reply: int | None = None
    is_locked: bool = False

    @classmethod
    def from_query_result(cls, topic_id, title, category_id, user_id, creation_date, best_reply, is_locked):
        return cls(
            id=topic_id,
            title=title,
            category_id=category_id,
            user_id=user_id,
            creation_date=creation_date,
            best_reply=best_reply,
            is_locked=is_locked
        )


class CreateTopic(BaseModel):
    title: str
    category_id: int


class Category(BaseModel):
    category_id: int
    name: str = constr(pattern="^\w{1,50}$")
    is_locked: bool
    is_private: bool

    @classmethod
    def from_query_result(cls, category_id, name, is_locked, is_private):

        return cls(
            category_id=category_id,
            name=name,
            is_locked=is_locked,
            is_private=is_private
        )


class CreateCategory(BaseModel):
    name: str = constr(pattern="^\w{1,50}$")


class CategoryWithTopics(BaseModel):
    category_id: int
    name: str = constr(pattern="^\w{1,50}$")
    is_locked: bool
    is_private: bool
    topics: list[Topic | None]


class Reply(BaseModel):
    id: int
    text: str
    topic_id: int
    user_id: int
    creation_date: datetime

    @classmethod
    def from_query_result(cls, reply_id, text, topic_id, user_id, creation_date):
        return cls(
            id=reply_id,
            text=text,
            topic_id=topic_id,
            user_id=user_id,
            creation_date=creation_date
        )


class CreateReply(BaseModel):
    text: str


class ChooseBestReply(BaseModel):
    reply_id: int


class ReplyWithVotes(BaseModel):
    id: int
    text: str
    topic_id: int
    user_id: int
    creation_date: datetime
    vote_type: int


class TopicWithReplies(BaseModel):
    category_id: int
    title: str
    user_id: int
    best_reply: int | None
    is_locked: bool
    replies: list[Reply | None]


class Vote(BaseModel):
    id: int
    reply_id: int
    user_id: int
    vote_type: bool | None


class Message(BaseModel):
    id: int
    text: str
    sender_id: int
    receiver_id: int
    creation_date: datetime

    @classmethod
    def from_query_result(cls, message_id, text, sender_id, receiver_id, creation_date):
        return cls(
            id=message_id,
            text=text,
            sender_id=sender_id,
            receiver_id=receiver_id,
            creation_date=creation_date
        )


class CreateMessage(BaseModel):
    text: str


class User(BaseModel):
    id: int
    username: str = constr(pattern="^\w{5,20}$")
    password: str = constr(pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    name: str = constr(pattern="^\w{2,25}$")
    is_admin: bool = False

    @classmethod
    def from_query_result(cls, user_id, username, password, email, name, is_admin=False):
        return cls(
            id=user_id,
            username=username,
            password=password,
            email=email,
            name=name,
            is_admin=is_admin
        )


class GetUser(BaseModel):
    id: int
    username: str = constr(pattern="^\w{5,20}$")
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    name: str = constr(pattern="^\w{2,25}$")

    @classmethod
    def from_query_result(cls, user_id, username, email, name):
        return cls(
            id=user_id,
            username=username,
            email=email,
            name=name,
        )


class UserCategoryAccess(BaseModel):
    user_id: int
    username: str
    access_level: str

    @classmethod
    def from_query_result(cls, user_id, username, access_level):
        return cls(user_id=user_id,
                   username=username,
                   access_level=access_level
                   )


class LoginInformation(BaseModel):
    username: str
    password: str
    email: str = None or None
    name: str = None or None
    is_admin: bool = False
